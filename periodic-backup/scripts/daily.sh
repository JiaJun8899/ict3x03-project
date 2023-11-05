#!/bin/sh

BACKUP_FOLDER=/var/backups/
NOW=$(date '+%d')

### MySQL Server Login info ###
MDB=$MYSQL_DATABASE
MHOST=$MYSQL_CONTAINER_NAME
MPASS=$DB_PASSWORD
MUSER=$DB_USER

[ ! -d "$BACKUP_FOLDER" ] && mkdir --parents $BACKUP_FOLDER

FILE=${BACKUP_FOLDER}/backup-${NOW}.sql
mariadb-dump --host $MHOST --databases $MDB --user=$MUSER --password=$MPASS > $FILE
