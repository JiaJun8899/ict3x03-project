# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-bullseye

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
   libmariadb-dev-compat gcc && \
   rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app/backend

# Copy the current directory contents into the container at /app/backend
COPY ./backend /app/backend
COPY ./requirements.txt /app/backend

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Make scripts executable
RUN chmod +x script/Entrypoint.sh && \
    chmod +x script/Migrations.sh && \
    chmod +x script/CollectStatic.sh

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Make scripts executable
RUN chmod +x script/Entrypoint.sh && \
    chmod +x script/Migrations.sh && \
    chmod +x script/CollectStatic.sh

# Run initialisation scripts
RUN bash script/CollectStatic.sh

# RUN bash script/Mi
