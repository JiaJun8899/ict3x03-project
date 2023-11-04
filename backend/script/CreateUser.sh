#!/bin/bash
# SQL commands to create the user and grant privileges
SQL_COMMANDS="
CREATE USER IF NOT EXISTS '${DB_USER_1}'@'%' IDENTIFIED BY '${DB_PASSWORD_1}';
GRANT ALL PRIVILEGES ON test_${DB_NAME}.* TO '${DB_USER_1}'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER ON ${DB_NAME}.* TO '${DB_USER_1}'@'%';
FLUSH PRIVILEGES;
"
# Execute SQL commands
mariadb -u"${DB_USER}" -p"${DB_PASSWORD}" -e "${SQL_COMMANDS}"

echo "User '${NEW_USER}' created with CRUD privileges on database '${DB_NAME}'."

