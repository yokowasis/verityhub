FROM python:3.10

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY . /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "3000", "--proxy-headers", "--workers", "4"]
