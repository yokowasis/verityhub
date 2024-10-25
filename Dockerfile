FROM python:3.10

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/app
COPY assets /code/app/assets

CMD ["fastapi", "run", "app/main.py", "--port", "3000", "--proxy-headers", "--workers", "4"]