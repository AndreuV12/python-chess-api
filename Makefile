# .PHONY: run
libs:
	@echo "Installing libraries..."
	pip install --upgrade pip
	pip install --progress-bar on --no-cache-dir -r ./requirements.txt

setpath:
	export PYTHONPATH="/Users/andreu/python-chess-api/app/"

run:
	@echo "RUNING APP"
	export PYTHONPATH="./app/"
	uvicorn app.main:app --reload

revision:
	@read -p "Msg: " msg; \
	alembic revision --autogenerate -m "$$msg"

freeze:
	pip freeze > requirements.txt


docker-build:
	docker-compose build

docker-up:
	docker-compose up

docker-down:
	docker-compose down

# Puedes agregar otras tareas aquí, por ejemplo, para ejecutar tests o migraciones
