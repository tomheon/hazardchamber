env:
	virtualenv -p python2.7 --no-site-packages env

env_req: env requirements.txt
	env/bin/pip install -r requirements.txt

lint:
	env/bin/flake8 *.py

test:
	env/bin/nosetests

.PHONY: env_req lint test
