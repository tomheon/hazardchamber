env:
	virtualenv -p python2.7 --no-site-packages env

install_requirements: env requirements.txt
	env/bin/pip install -r requirements.txt

lint:
	env/bin/flake8 *.py tests

test:
	env/bin/nosetests

.PHONY: env_req lint test
