#!/bin/sh

python /usr/src/app/wait_for.py
pytest /usr/src/app/src/*.py
