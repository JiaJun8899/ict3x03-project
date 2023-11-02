# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-bullseye

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
   libmariadb-dev-compat gcc                   `: MySQL client` \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend
COPY ./backend /app/backend

RUN pip install pip --upgrade && \
    pip install -r requirements.txt && \ 
    chmod +x script/Entrypoint.sh && \
    chmod +x script/Migrations.sh && \
    chmod +x script/Collectstatic.sh && \
    chmod +x script/CreateUser.sh && \
    bash script/CreateUser.sh && \
    bash script/collectstatic.sh && \
    bash script/migrations.sh

CMD ["script/Entrypoint.sh"]