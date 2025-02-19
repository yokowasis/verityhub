FROM python:3.10

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY . /code

RUN curl -fsSL https://ollama.com/install.sh | sh
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN chmod a+x /code/start.sh

CMD ["start.sh"]