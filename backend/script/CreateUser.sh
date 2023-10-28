#!/bin/bash

# New user details
NEW_USER=$DB_USER_1
NEW_USER_PASSWORD=$DB_PASSWORD_1
DB_NAME=$DB_NAME

# SQL commands to create the user and grant privileges
SQL_COMMANDS="
CREATE USER IF NOT EXISTS'${NEW_USER}'@'localhost' IDENTIFIED BY '${NEW_USER_PASSWORD}';
GRANT SELECT, INSERT, UPDATE, DELETE ON ${DB_NAME}.* TO '${NEW_USER}'@'localhost';
FLUSH PRIVILEGES;
"

# Execute SQL commands
mariadb -u"${DB_USER}" -p"${DB_PASSWORD}" -e "${SQL_COMMANDS}"

echo "User '${NEW_USER}' created with CRUD privileges on database '${DB_NAME}'."