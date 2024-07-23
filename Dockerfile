FROM python:3.12

WORKDIR /automaestro

COPY requirements.txt .

RUN python -m pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY . .
