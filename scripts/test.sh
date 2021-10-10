#!/usr/bin/bash

arg=${1:-"not integration"}

poetry run python -m pytest -v --cov=markdownusm --cov-report=xml --capture=no -k "$arg"