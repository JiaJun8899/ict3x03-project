FROM alpine:latest

COPY ./periodic-backup/scripts/daily.sh /etc/periodic/daily

RUN apk update && \
    apk upgrade && \
    apk add --no-cache mariadb-client && \
    chmod a+x /etc/periodic/daily/*