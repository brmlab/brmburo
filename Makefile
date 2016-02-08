MANAGE=bin/python manage.py
PROJECT_NAME=brmburo
FLAKE8_OPTS=--exclude=.git,migrations --max-complexity=10
SETTINGS=--settings=$(PROJECT_NAME).settings.test
PIP ?= bin/pip
VIRTUALENV ?= virtualenv

.PHONY : clean rmenv all test coverage ensure_virtualenv

all: coverage

rmall: rmenv
	rm -fr tmp

rmenv: clean
	rm -fr bin lib local include build initenv share man pip-selfcheck.json

tmp:
	mkdir tmp

initenv: tmp
	$(VIRTUALENV) .
	$(VIRTUALENV) . --relocatable
	$(VIRTUALENV) . --system-site-packages
	echo '# Environment initialization placeholder. Do not delete. Use "make rmenv" to remove environment.' > $@

ensure_virtualenv:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "Please run me inside virtualenv.";  \
		exit 1; \
	fi

test: initenv
	$(MANAGE) test --where=. $(SETTINGS) --with-xunit

coverage: initenv
	$(MANAGE) test --where=. $(SETTINGS) \
		--with-xcoverage --with-xunit --cover-html  --cover-erase
lint: initenv
	flake8 $(FLAKE8_OPTS) .


clean:
	find . -name '*.pyc' -exec rm '{}' ';'

reqs/%: initenv
	$(PIP) install  --download-cache=tmp/cache --src=tmp/src -r requirements/$*.txt

setup/dev: initenv reqs/dev
	if [ ! -f $(PROJECT_NAME)/settings/local.py ]; then \
		echo 'from .dev import *' > $(PROJECT_NAME)/settings/local.py; \
	fi
	$(MANAGE) syncdb --all
	$(MANAGE) migrate --fake

setup/prod setup/test: initenv reqs/prod
	$(MAKE) update

update/dev: initenv reqs/dev
	$(MAKE) update

update: initenv
	$(MAKE) clean
	$(MANAGE) syncdb
	$(MANAGE) migrate
	$(MANAGE) collectstatic --noinput

load: load/static load/account load/buddy

load/%:
	$(MANAGE) loaddata $* 

migrate-init/%: initenv
	$(MANAGE) schemamigration $* --initial
	$(MANAGE) migrate $* --fake --delete-ghost-migrations

migrate-update/%: initenv
	$(MANAGE) schemamigration $*  --auto
	$(MANAGE) migrate $*
