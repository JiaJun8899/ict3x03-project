FROM mariadb:latest

EXPOSE 3306

# Expose the default MariaDB port

# Copy the initialization script to the Docker entrypoint directory
COPY ./backend/script/CreateUser.sh /docker-entrypoint-initdb.d/
# After the COPY command
RUN chmod +x /docker-entrypoint-initdb.d/CreateUser.sh


