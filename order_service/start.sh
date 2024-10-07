#!/bin/sh


flask db init
flask db migrate -m "Initial migration"
flask db upgrade &

python manage.py &

python consumer.py

wait
