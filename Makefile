format:
	yapf -ri grep/
	yapf -ri tests/

ifeq ($(shell uname), $(or Linux, Darwin))
test: clean
	pytest -vv --ignore=venv2/ --ignore=venv3/
test2: clean
	pytest2 -vv --ignore=venv2/ --ignore=venv3/

test-report: clean
	pytest -vv --cov-report term-missing:skip-covered --cov=grep/ --ignore=venv2/ --ignore=venv3/
test-report2: clean
	pytest2 -vv --cov-report term-missing:skip-covered --cov=grep/ --ignore=venv2/ --ignore=venv3/

clean:
	rm -f */**.pyc */*/**.pyc

clean_virtualenv:
	rm -rf venv3/
clean_virtualenv2:
	rm -rf venv2/

new_virtualenv: clean_virtualenv
	virtualenv -p /usr/bin/python3.6 venv3/
new_virtualenv2: clean_virtualenv2
	virtualenv -p /usr/bin/python2.7 venv2/


else
test: clean
	python -m pytest -vv --ignore=venv2/ --ignore=venv3/
clean:
	del /s /q *.pyc

endif

