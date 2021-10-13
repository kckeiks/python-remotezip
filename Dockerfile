# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /app
# ENV FLASK_APP=app.py I think therse are env variables that the contianer will have access too
# ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
# CMD ["python3", "runcmd.py", "--help"]
