ifeq ($(shell uname), $(or Linux, Darwin))
clean:
	rm -f */**.pyc
	rm -f */*/**.pyc

test: clean
	py.test -vv --ignore=venv/

test-report: clean
	py.test -vv --cov-report term-missing:skip-covered --cov=grep/ --ignore=venv/


test2: clean
	pytest2 -vv --ignore=venv/

test2-report: clean
	pytest2 -vv --cov-report term-missing:skip-covered --cov=grep/ --ignore=venv/


else
clean:
	del /s /q *.pyc

test: clean
	py.test -vv

endif
