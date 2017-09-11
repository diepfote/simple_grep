ifeq ($(shell uname), $(or Linux, Darwin))
test: clean
	pytest -vv --ignore=venv2/ --ignore=venv3/

test-report: clean
	pytest -vv --cov-report term-missing:skip-covered --cov=grep/ --ignore=venv2/ --ignore=venv3/

test2: clean
	pytest2 -vv --ignore=venv2/ --ignore=venv3/

test-report2: clean
	pytest2 -vv --cov-report term-missing:skip-covered --cov=grep/ --ignore=venv2/ --ignore=venv3/


clean:
	rm -f */**.pyc */*/**.pyc

clean_venv2:
	rm -rf venv2/

clean_venv:
	rm -rf venv3/


new_virtualenv: clean_venv
	virtualenv -p /usr/bin/python3.6 venv3/

new_virtualenv2: clean_venv2
	virtualenv -p /usr/bin/python2.7 venv2/


install:
	pip3 install -e .

uninstall:
	pip3 uninstall simple_grep

install2:
	pip2 install -e .

uninstall2:
	pip2 uninstall simple_grep


test: clean
	pytest -vv --ignore=venv2/ --ignore=venv3/

test-report: clean
	pytest -vv --cov-report term-missing:skip-covered --cov=grep/ --ignore=venv2/ --ignore=venv3/

test2: clean
	pytest2 -vv --ignore=venv2/ --ignore=venv3/

test2-report: clean
	pytest2 -vv --cov-report term-missing:skip-covered --cov=grep/ --ignore=venv2/ --ignore=venv3/




else
test: clean
	python -m pytest -vv --ignore=venv2/ --ignore=venv3/
clean:
	del /s /q *.pyc

endif

