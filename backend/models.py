from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from pydantic import BaseModel
from database import Base

# --- MODELOS DE SQLALCHEMY (Definición de Tablas) ---

class User(Base):
    """Representa la tabla de usuarios."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación con las partidas: un usuario puede tener muchas partidas.
    # El back_populates enlaza con la relación en la clase Game.
    games_as_player1 = relationship("Game", foreign_keys="[Game.player1_id]", back_populates="player1")
    games_as_player2 = relationship("Game", foreign_keys="[Game.player2_id]", back_populates="player2")


class Game(Base):
    """Representa la tabla de partidas de Batalla Naval."""
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    
    # El estado de la partida se serializará como JSON/Texto
    game_state = Column(String, default="INITIALIZED") 
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    # Jugador 1
    player1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Jugador 2 (opcional, puede ser NULL si está esperando o jugando contra IA)
    player2_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relaciones para obtener el objeto User directamente
    player1 = relationship("User", foreign_keys=[player1_id], back_populates="games_as_player1")
    player2 = relationship("User", foreign_keys=[player2_id], back_populates="games_as_player2")


# --- MODELOS DE PYDANTIC (Esquemas para I/O) ---

class UserBase(BaseModel):
    """Esquema base para un usuario (para creación)."""
    username: str

class UserCreate(UserBase):
    """Esquema de creación de usuario."""
    pass

class UserInDB(UserBase):
    """Esquema para un usuario leído de la base de datos."""
    id: int
    created_at: datetime

    class Config:
        # Habilita el mapeo automático a objetos SQLAlchemy
        from_attributes = True

class GameBase(BaseModel):
    """Esquema base para una partida."""
    game_state: str = "INITIALIZED"
    is_active: bool = True

class GameInDB(GameBase):
    """Esquema para una partida leída de la base de datos."""
    id: int
    player1_id: int
    player2_id: Optional[int] = None
    created_at: datetime
    finished_at: Optional[datetime] = None

    # Opcional: Incluir los objetos User completos si se cargan las relaciones
    player1: UserInDB
    player2: Optional[UserInDB] = None

    class Config:
        from_attributes = True