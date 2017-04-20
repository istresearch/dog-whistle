#!/bin/bash
# Script to build the dog-whistle distribution, and push to pypi

python setup.py sdist
twine upload dist/dog-whistle-*.tar.gz
rm -rf dist/*