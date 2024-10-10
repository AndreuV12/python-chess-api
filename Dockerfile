# Usa una imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt y el código de tu aplicación al contenedor
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala Stockfish
RUN apt-get update && \
    apt-get install -y stockfish && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia el resto de tu código al contenedor
COPY . .

# Comando para ejecutar tu aplicación
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
