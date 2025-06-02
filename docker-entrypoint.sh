#!/bin/bash
set -e

echo "Applying migrations"
pipenv run alembic upgrade head
echo "Done"

echo "Starting application"
exec "$@"
