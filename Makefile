ifeq ($(shell uname), $(or Linux, Darwin))
clean:
	rm -f */**.pyc
	rm -f */*/**.pyc

test: clean
	pytest -vv --ignore=venv/

test-report: clean
	pytest2 -vv --cov-report term-missing:skip-covered --cov=grep/ --ignore=venv/


else
clean:
	del /s /q *.pyc

test: clean
	py.test -vv


endif
