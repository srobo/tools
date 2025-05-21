#!/bin/bash

cd $(dirname $(dirname  $(dirname $0)))

exec python setup.py build_sphinx "$@"
