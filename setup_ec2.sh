#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install pypy python-virtualenv tmux
virtualenv --no-site-packages -p pypy env
