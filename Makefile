export DJANGO_SETTINGS_MODULE = tests.mockapp.settings
export PYTHONPATH := $(shell pwd)

.PHONY: help
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

.PHONY: clean
clean:
	git clean -Xfd

.PHONY: develop
develop:
	pip install -r requirements.dev.txt

.PHONY: shell
shell:
	django-admin.py shell

.PHONY: test
test:
	django-admin.py test tests

.PHONY: migrations
migrations:
	django-admin.py makemigrations tidings

.PHONY: docs
docs:
	$(MAKE) -C docs clean html

.PHONY: test-all
test-all:
	tox --skip-missing-interpreters

.PHONY: coverage
coverage:
	coverage erase
	coverage run --branch --source=tidings `which django-admin` test tests

.PHONY: coveragehtml
coveragehtml: coverage
	coverage html
	python -m webbrowser file://$(CURDIR)/htmlcov/index.html

.PHONY: lint
lint:
	flake8 .

.PHONY: qa
qa: lint coveragehtml

.PHONY: qa-all
qa-all: qa sdist test-all

.PHONY: sdist
sdist:
	python setup.py sdist bdist_wheel
	ls -l dist
	check-manifest
	pyroma dist/`ls -t dist | grep tar.gz | head -n1`

.PHONY: release
release: clean sdist
	gpg --detach-sign -a dist/*.tar.gz
	gpg --detach-sign -a dist/*.whl
	twine upload dist/*
	python -m webbrowser -n https://pypi.python.org/pypi/django-tidings

.PHONY: test-release
# Add [test] section to ~/.pypirc, https://testpypi.python.org/pypi
test-release: clean sdist
	gpg --detach-sign -a dist/*.tar.gz
	gpg --detach-sign -a dist/*.whl
	twine upload --repository test dist/*
	python -m webbrowser -n https://testpypi.python.org/pypi/django-tidings
