#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install build dependencies FIRST
pip install --upgrade pip setuptools wheel

# 2. Then install your project requirements
pip install -r requirements.txt

# 3. Run Django commands
python manage.py collectstatic --no-input
python manage.py migrate