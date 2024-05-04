#!/bin/bash

# export all variables from .env file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";
PARENT_DIRECTORY="${DIR%/*}"

PGPASSWORD=$DB_PASS psql --username=postgres -h localhost -p 5432 data < $PARENT_DIRECTORY/ds/dump.sql