FROM python:3.12

COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt -r requirements-dev.txt