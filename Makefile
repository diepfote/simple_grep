ifeq ($(shell uname), $(or Linux, Darwin))
clean:
	rm -f */**.pyc
	rm -f */*/**.pyc


clean_venv2:
	rm -rf venv2/

clean_venv:
	rm -rf venv3/

new_virtualenv:
	virtualenv2 -p /usr/bin/python3.6 venv3/
	chmod +x venv3/bin/activate
	./venv3/bin/activate

new_virtualenv2:
	virtualenv2 -p /usr/bin/python2.7 venv2/
	chmod +x venv2/bin/activate
	./venv2/bin/activate


install: clean_venv new_virtualenv
	pip3 install -r requirements.txt
	sudo pip3 install -e .

install2: clean_venv2 new_virtualenv2
	pip2 install -r requirements.txt
	sudo pip2 install -e .


uninstall:
	sudo pip3 uninstall simple_grep

uninstall2:
	sudo pip2 uninstall simple_grep



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
