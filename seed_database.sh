#!/bin/bash

rm db.sqlite3
rm -rf ./whereandwhenapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations whereandwhenapi
python3 manage.py migrate whereandwhenapi
python3 manage.py loaddata users.json
python3 manage.py loaddata groupreps.json
python3 manage.py loaddata grouprepmeetings.json
python3 manage.py loaddata meetings.json
python3 manage.py loaddata days.json
python3 manage.py loaddata meetingdays.json
python3 manage.py loaddata types.json
python3 manage.py loaddata districts.json
python3 manage.py loaddata areas.json