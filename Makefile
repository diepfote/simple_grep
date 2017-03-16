clean:
	rm -f */**.pyc

test: clean
	pytest2 -vv

test-report: clean
	pytest2 -vv --cov-report term-missing --cov=grep_redone/grep/
