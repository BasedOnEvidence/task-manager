include task_manager/.env

CURRENT_BRANCH = $(shell git rev-parse --abbrev-ref HEAD)
CREATE_ENV = $(shell test ! -f ./task_manager/.env && cp ./task_manager/template.env ./task_manager/.env)

install:
	poetry install

create_env:
	$(CREATE_ENV)

update:
	poetry update

build:
	poetry build

lint:
	poetry run flake8 page_loader

tests:
	poetry run pytest -vv -s

coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml
	poetry run coverage report

start:
	python3 manage.py runserver

gunicorn:
	poetry run gunicorn task_manager.wsgi

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

.PHONY: task_manager tests

language:
	django-admin makemessages -l en
	django-admin makemessages -l ru

locale:
	django-admin compilemessages

push:
	git add .
	git commit -m "$(commit)"
	git push --set-upstream origin $(CURRENT_BRANCH)

heroku:
	heroku config:set SECRET_KEY=$(SECRET_KEY) --app task-manager-template
	heroku config:set DEBUG=$(DEBUG) --app task-manager-template
	git push heroku main:main
	heroku run make migrate --app task-manager-template
