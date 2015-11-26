install_requirements: env requirements.txt
	env/bin/pip install -r requirements.txt

env:
	virtualenv -p python2.7 --no-site-packages env

lint:
	env/bin/flake8 *.py tests

test:
	env/bin/nosetests

.PHONY: install_requirement lint test
