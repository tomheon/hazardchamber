#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y pypy python-virtualenv tmux
virtualenv --no-site-packages -p pypy env
