export DJANGO_SETTINGS_MODULE = tests.settings
export PYTHONPATH := $(shell pwd)

clean:
	git clean -Xfd

shell:
	django-admin.py shell

test:
	django-admin.py test tests

migrations:
	django-admin.py makemigrations tidings

docs:
	$(MAKE) -C docs clean html

.PHONY: clean shell migrations docs test
