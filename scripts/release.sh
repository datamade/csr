#!/bin/bash
set -euo pipefail

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py loaddata data/fixtures/initial_user
