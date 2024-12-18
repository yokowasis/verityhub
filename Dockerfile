FROM yokowasis/verityhub-base:latest

WORKDIR /code
COPY . /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "3000", "--proxy-headers", "--workers", "4"]
