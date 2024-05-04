#!/bin/bash

# export all variables from .env file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";
PARENT_DIRECTORY="${DIR%/*}"
set -o allexport 
source $PARENT_DIRECTORY/.env
set +o allexport 


# export database
PGPASSWORD=$DB_PASS pg_dump -U $DB_USER -h $DB_HOST $DB_NAME --no-privileges --no-owner  > $PARENT_DIRECTORY/ds/dump.sql