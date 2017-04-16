ifeq ($(shell uname), $(or Linux, Darwin))
clean:
	rm -f */**.pyc
	rm -f */*/**.pyc

test: clean
	pytest -vv --ignore=venv2/ --ignore=venv3/

test-report: clean
	pytest -vv --cov-report term-missing:skip-covered --cov=grep/ --ignore=venv2/ --ignore=venv3/


test2: clean
	pytest2 -vv --ignore=venv2/ --ignore=venv3/

test2-report: clean
	pytest2 -vv --cov-report term-missing:skip-covered --cov=grep/ --ignore=venv2/ --ignore=venv3/


else
clean:
	del /s /q *.pyc

test: clean
	py.test -vv

endif
