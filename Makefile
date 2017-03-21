export DJANGO_SETTINGS_MODULE = tests.settings
export PYTHONPATH := $(shell pwd)

help:
	@echo "clean - remove all artifacts"
	@echo "coverage - check code coverage"
	@echo "coveragehtml - display code coverage in browser"
	@echo "develop - install development requirements"
	@echo "lint - check style with flake8"
	@echo "qa - run linters and test coverage"
	@echo "qa-all - run QA plus packaging and cross-version tests"
	@echo "release - package and upload a release"
	@echo "sdist - package"
	@echo "test - run tests"
	@echo "test-all - run tests against eacy Django/Python version"
	@echo "test-release - upload a release to the test PyPI server"

clean:
	git clean -Xfd

develop:
	pip install -r requirements.dev.txt

shell:
	django-admin.py shell

test:
	django-admin.py test tests

migrations:
	django-admin.py makemigrations tidings

docs:
	$(MAKE) -C docs clean html

test-all:
	tox --skip-missing-interpreters

coverage:
	coverage erase
	coverage run --branch --source=tidings `which django-admin` test tests

coveragehtml: coverage
	coverage html
	python -m webbrowser file://$(CURDIR)/htmlcov/index.html

lint:
	flake8 .

qa: lint coveragehtml

qa-all: qa sdist test-all

sdist:
	python setup.py sdist bdist_wheel
	ls -l dist
	check-manifest
	pyroma dist/`ls -t dist | grep tar.gz | head -n1`

release: clean sdist
	twine register dist/*.tar.gz
	twine register dist/*.whl
	twine upload dist/*
	python -m webbrowser -n https://pypi.python.org/pypi/django-tidings

# Add [test] section to ~/.pypirc, https://testpypi.python.org/pypi
test-release: clean sdist
	twine register --repository test dist/*.tar.gz
	twine register --repository test dist/*.whl
	twine upload --repository test dist/*
	python -m webbrowser -n https://testpypi.python.org/pypi/django-tidings

.PHONY: help clean coverage coveragehtml develop lint qa qa-all release sdist test test-all test-release
