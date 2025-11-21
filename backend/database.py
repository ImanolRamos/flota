from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Configuración de PostgreSQL ---
# ¡IMPORTANTE! Reemplaza estos valores por los de tu configuración local de PostgreSQL
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "your_postgres_password"  # <-- Cambia esto
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "battleship_db"

# Cadena de conexión asíncrona para asyncpg
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Motor de la base de datos asíncrono
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=True  # Muestra las consultas SQL en la consola (útil para desarrollo)
)

# Objeto Base para los modelos declarativos
Base = declarative_base()

# Sesión asíncrona de la base de datos
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Para que los objetos no expiren tras un commit
)

async def get_async_session():
    """Dependencia para obtener una sesión de base de datos."""
    async with AsyncSessionLocal() as session:
        yield session

async def create_db_and_tables():
    """Crea las tablas en la base de datos (si no existen)."""
    async with engine.begin() as conn:
        # Importa Base y los modelos antes de llamar a este método
        # para que SQLAlchemy conozca todas las tablas
        import models  
        await conn.run_sync(Base.metadata.create_all)