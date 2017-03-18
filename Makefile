clean:
	rm -f */**.pyc

test: clean
	py.test -vv

test-report: clean
	py.test -vv --cov-report term-missing --cov=grep_redone/grep/
