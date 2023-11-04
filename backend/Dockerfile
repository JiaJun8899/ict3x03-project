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

# Install pip requirements
COPY /requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app/backend
COPY ./backend /app/backend

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Make scripts executable
RUN chmod +x script/Entrypoint.sh && \
    chmod +x script/Migrations.sh && \
    chmod +x script/CollectStatic.sh

# Run initialisation scripts
RUN bash script/CollectStatic.sh

# RUN bash script/Migrations.sh

# Run the application

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]