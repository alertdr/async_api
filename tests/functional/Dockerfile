FROM python:3.10.2-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 9200:9200
EXPOSE 6379:6379

WORKDIR /usr/src/app

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm requirements.txt

COPY utils/wait_for.py .
COPY src/. /usr/src/app/src

ENTRYPOINT python /usr/src/app/wait_for.py && pytest /usr/src/app/src/*.py
