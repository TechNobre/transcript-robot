FROM python:3.12.4-slim

RUN apt-get update && apt-get install -y \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src .

CMD ["python", "App.py"]
