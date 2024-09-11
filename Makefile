
PROJECT_DIR := $(shell pwd)

run:
    @export PYTHONPATH=$(PROJECT_DIR) && uvicorn app.main:app --reload

# Puedes agregar otras tareas aquí, por ejemplo, para ejecutar tests o migraciones
