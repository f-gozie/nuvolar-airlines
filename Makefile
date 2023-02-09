build:
				docker compose -f local.yml build

clean:  clean-pyc
				docker compose down -v --remove-orphans
				docker compose -f local.yml down -v --remove-orphans

clean-pyc:
				sudo find . -name '*.pyc' -exec rm -f {} +
				sudo find . -name '*.pyo' -exec rm -f {} +
				sudo find . -name '*~' -exec rm -f {} +
				sudo find . -name '__pycache__' -exec rm -fr {} +
				sudo rm -fr src/.ipython

down:
				docker compose -f local.yml down --remove-orphans
				docker compose -f local.yml down --remove-orphans

up-detached: down
				docker compose -f local.yml up -d

up: down
				docker compose -f local.yml up

shell:
				docker compose -f local.yml run --rm django python manage.py shell

bash:
				docker compose -f local.yml run --rm django /bin/bash

dbshell:
				docker compose -f local.yml run --rm django python manage.py dbshell

migrate:
				docker compose -f local.yml run --rm django python manage.py migrate

migrations:
				docker compose -f local.yml run --rm django python manage.py makemigrations

pre-commit:
				pre-commit run --all-files

debug:
				docker compose -f local.yml run --rm --service-ports django


show-urls:
				docker compose -f local.yml run --rm django python manage.py show_urls

test:
				docker compose -f local.yml run --rm django pytest

push:
				git push --set-upstream origin $(branch)

backup:
				docker compose -f local.yml run --rm postgres backup

backups:
				docker compose -f local.yml run --rm postgres backups

restore:
				docker compose -f local.yml run --rm postgres restore $(file)

restore-from-dump:
				docker compose -f local.yml run --rm postgres restore-from-dump $(file)
