FROM python:3.8
WORKDIR /code/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN python -m pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./main.py /code/main.py

EXPOSE 7000
