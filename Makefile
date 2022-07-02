CURRENT_BRANCH = $(shell git rev-parse --abbrev-ref HEAD)

install:
	poetry install
	export DJANGO_SETTINGS_MODULE=hello_django.settings

update:
	poetry update

build:
	poetry build

lint:
	poetry run flake8 page_loader

tests:
	poetry run pytest -vv -s

start:
	python3 manage.py runserver

gunicorn:
	poetry run gunicorn task_manager.wsgi

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

.PHONY: task_manager tests

language:
	cd task_manager
	django-admin makemessages -l en
	django-admin makemessages -l ru

locale:
	cd task_manager
	django-admin compilemessages

push:
	git add .
	git commit -m "$(commit)"
	git push --set-upstream origin $(CURRENT_BRANCH)