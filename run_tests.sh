#!/bin/bash
set -e
nosetests --nocapture -v --with-coverage --cover-package=dog_whistle --cover-xml --cover-erase
python setup.py sdist