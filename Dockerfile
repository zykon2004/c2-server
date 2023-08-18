FROM python:3.11.4-bullseye

WORKDIR /c2-server

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./server ./server
COPY ./resources ./resources

ADD  https://github.com/zykon2004/c2-server-cli /

# WORKDIR /c2-server-cli
# RUN pip install --no-cache-dir --upgrade -r requirements.txt


EXPOSE 8080-8080

CMD ["python", "server/server.py"]
