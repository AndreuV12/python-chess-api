from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

# Construir la URL de conexión usando la configuración
SQLALCHEMY_DATABASE_URL = settings.get_database_url()

# Crear el motor de SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear una clase SessionLocal que puede ser utilizada para crear sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
