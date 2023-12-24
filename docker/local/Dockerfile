FROM python:3.11
WORKDIR /bot

COPY ./requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./src ./src

WORKDIR /bot/src

CMD alembic --config ./alembic/alembic.ini upgrade head && python3 main.py