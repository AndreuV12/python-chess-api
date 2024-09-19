# .PHONY: run
libs:
	@echo "Installing libraries..."
	pip install --upgrade pip
	pip install --progress-bar on --no-cache-dir -r ./app/api/requirements_dev.txt

setpath:
	export PYTHONPATH="./app/"

run:
	@echo "RUNING APP"
	export PYTHONPATH="./app/"
	uvicorn app.main:app --reload

revision:
	@read -p "Msg: " msg; \
	alembic revision --autogenerate -m "$$msg"

freeze:
	pip freeze > requirements.txt

# Puedes agregar otras tareas aquí, por ejemplo, para ejecutar tests o migraciones
