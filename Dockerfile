FROM yokowasis/verityhub-base:latest

WORKDIR /code
COPY . /code

CMD ["/code/start.sh"]