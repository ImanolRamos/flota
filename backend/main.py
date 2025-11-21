import socketio, os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# FRONTEND_ORIGIN = "http://192.168.2.104:5173"
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:8080")
LISTEN_PORT = int(os.getenv("LISTEN_PORT", 3003))

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[FRONTEND_ORIGIN])
socket_app = socketio.ASGIApp(sio)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/socket.io", socket_app)

rooms = {}

@app.get("/")
def root():
    return {"message": "Servidor hundir la flota listo"}

@sio.event
async def connect(sid, environ):
    print(f"[{sid}] conectado")

@sio.event
async def disconnect(sid):
    print(f"[{sid}] desconectado")
    for room_id, state in list(rooms.items()):
        if sid in state["players"]:
            # Obtener el SID del oponente
            opponent_sids = [p for p in state["players"] if p != sid]
            
            # Si hay un oponente, notificarle que el otro jugador se fue
            if opponent_sids:
                await sio.emit("opponent_left", {}, room=opponent_sids[0])
            
            # Cerrar y eliminar la sala
            await sio.close_room(room_id)
            rooms.pop(room_id, None)
            break

# --- FUNCIÓN AUXILIAR AÑADIDA ---
def get_players_data(state):
    """Prepara los datos esenciales de los jugadores (sid, name) para enviar al cliente."""
    players_data = []
    for sid, player_info in state["players"].items():
        players_data.append({
            "sid": sid,
            "name": player_info["name"]
        })
    return players_data
# --------------------------------

@sio.event
async def create_room(sid, data):
    print("Evento create_room:", sid, data)
    room_id = data["roomId"]
    name = data.get("name", "Jugador")
    
    rooms[room_id] = {
        "players": {sid: {"name": name, "ready": False, "board": {}, "hits": set()}},
        "order": [sid],
        "turnIndex": 0,
        "started": False,
    }
    await sio.enter_room(sid, room_id)
    
    # 🎯 ARREGLO: Incluir la lista de jugadores en el payload
    state = rooms[room_id]
    players_data = get_players_data(state)
    await sio.emit("room_update", {"roomId": room_id, "players": players_data}, room=room_id)

@sio.event
async def join_room(sid, data):
    print("Evento join_room:", sid, data)
    room_id = data["roomId"]
    name = data.get("name", "Jugador")
    
    if room_id not in rooms:
        await sio.emit("error_message", {"error": "Sala no existe"}, room=sid)
        return

    state = rooms[room_id]
    
    # Validación: la sala no debe estar llena
    if len(state["order"]) >= 2:
        await sio.emit("error_message", {"error": "Sala llena"}, room=sid)
        return
        
    state["players"][sid] = {"name": name, "ready": False, "board": {}, "hits": set()}
    state["order"].append(sid)
    await sio.enter_room(sid, room_id)
    
    # 🎯 ARREGLO: Incluir la lista de jugadores en el payload (ahora hay dos)
    players_data = get_players_data(state)
    await sio.emit("room_update", {"roomId": room_id, "players": players_data}, room=room_id)

@sio.event
async def place_ships(sid, data):
    print("Evento place_ships:", sid, data)
    room_id = data["roomId"]
    board = data["board"]
    state = rooms[room_id]
    state["players"][sid]["board"] = board
    state["players"][sid]["ready"] = True
    await sio.emit("player_ready", {"sid": sid}, room=room_id)

    if len(state["order"]) == 2:
        s1, s2 = state["order"]
        if state["players"][s1]["ready"] and state["players"][s2]["ready"]:
            state["started"] = True
            await sio.emit("game_started", {"turn": state["order"][0]}, room=room_id)

@sio.event
async def fire(sid, data):
    print("Evento fire:", sid, data)
    # Aceptamos "RoomId" o "roomId" por robustez, pero es mejor estandarizarlo
    room_id = data.get("RoomId") or data["roomId"] 
    cell = data["cell"]
    state = rooms[room_id]
    current_sid = state["order"][state["turnIndex"]]
    
    if sid != current_sid:
        await sio.emit("error_message", {"error": "No es tu turno"}, room=sid)
        return

    opponent_sid = state["order"][1 - state["turnIndex"]]
    opponent = state["players"][opponent_sid]
    hit = False
    sunk = None

    for ship, cells in opponent["board"].items():
        if cell in cells:
            hit = True
            opponent["hits"].add(cell)
            if all(c in opponent["hits"] for c in cells):
                sunk = ship
            break

    await sio.emit("fire_result", {"by": sid, "cell": cell, "hit": hit, "sunk": sunk}, room=room_id)

    total_cells = sum(len(cells) for cells in opponent["board"].values())
    if len(opponent["hits"]) == total_cells and total_cells > 0:
        await sio.emit("game_over", {"winner": sid}, room=room_id)
        await sio.close_room(room_id)
        rooms.pop(room_id, None)
        return

    state["turnIndex"] = 1 - state["turnIndex"]
    await sio.emit("turn_changed", {"turn": state["order"][state["turnIndex"]]}, room=room_id)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=LISTEN_PORT, reload=True)