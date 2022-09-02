FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev libpq-dev

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt

EXPOSE 8050

CMD ["python3", "dash_main.py"]