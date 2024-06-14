#!/bin/bash
# Можно ли сделать это посимпатичнее

flake8
pydocstyle .
python -m unittest -v tests/*.py