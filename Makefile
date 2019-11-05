ENV_FILE := .env
include ${ENV_FILE}
export $(shell sed 's/=.*//' ${ENV_FILE})
export PIPENV_DOTENV_LOCATION=${ENV_FILE}

run_app_pipenv:
	pipenv run python app.py

run_test_pipenv:
	pipenv run python test_model.py

run_app:
	python app.py

run_test:
	python test_model.py
