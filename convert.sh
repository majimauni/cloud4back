#/bin/env bash

export RDS_DB_NAME='your_dbname'
export RDS_USERNAME='your_username'
export RDS_PASSWORD='your_password'
export DJANGO_SETTINGS_MODULE=cloudprojects.settings
echo DJANGO
python convertScript.py
