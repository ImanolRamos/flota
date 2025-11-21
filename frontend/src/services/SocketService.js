import { io } from "socket.io-client";
const SOCKET_URL = "http://192.168.2.104:3003";

const socket = io(SOCKET_URL, {
  autoConnect: false,
  transports: ["websocket"],
});

socket.on("connect", () => {
  console.log("✅ Conectado al servidor con id:", socket.id);
});

socket.on("connect_error", (err) => {
  console.error("❌ Error de conexión:", err.message);
});

export default {
  connect() { socket.connect(); },
  disconnect() { socket.disconnect(); },
  on(event, cb) { socket.on(event, cb); },
  emit(event, data) { socket.emit(event, data); },
  id() { return socket.id; },
};
