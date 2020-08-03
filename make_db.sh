#!/usr/bin/env bash

echo "Creating database wellread_db"

psql -c "CREATE USER wellread_user WITH PASSWORD '1234';"
psql -c "CREATE DATABASE wellread_db WITH OWNER wellread_user ENCODING 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' TEMPLATE template0;"
psql -c "GRANT ALL PRIVILEGES ON DATABASE wellread_db to wellread_user;"
psql -c "ALTER USER wellread_user CREATEDB;"

echo "Created database wellread_db with user wellread_user"