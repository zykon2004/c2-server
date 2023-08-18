FROM python:3.11.4-bullseye

WORKDIR /c2-server

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./server ./server
COPY ./resources ./resources

RUN git clone https://github.com/zykon2004/c2-server-cli.git /c2-server-cli

WORKDIR /c2-server-cli
RUN pip install -r /c2-server-cli/requirements.txt


EXPOSE 8001

CMD ["python", "/c2-server/server/server.py"]
