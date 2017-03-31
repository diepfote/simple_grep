ifeq ($(shell uname), $(or Linux, Darwin))
clean:
	rm -f */**.pyc
	rm -f */*/**.pyc

test: clean
	py.test -vv

test-report: clean
	py.test -vv --cov-report term-missing:skip-covered --cov=grep/


else
clean:
	del /s /q *.pyc

test: clean
	py.test -vv

endif
