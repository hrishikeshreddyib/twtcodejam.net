#!/bin/sh
set -e

folders="TWT"

set -x

# put every import on one line for autoflake remove unused imports
isort $folders --force-single-line-imports
# remove unused imports and variables
autoflake $folders --remove-all-unused-imports --recursive --remove-unused-variables --in-place --exclude=__init__.py

# format code
black $folders --line-length 120

# resort imports
isort $folders
