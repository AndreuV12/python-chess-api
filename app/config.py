from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Cargar las variables de entorno desde el archivo .env
load_dotenv(".env.local")


# Definir la clase de configuración
class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    STOCKFISH_PATH: str

    def get_database_url(self) -> str:
        print(
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


# Funcion para instanciar Settings para acceder a las variables de entorno
def get_settings():
    return Settings()
