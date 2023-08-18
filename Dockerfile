FROM python:3.11.4-bullseye

WORKDIR /c2-server

COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./server ./server
COPY ./resources ./resources

RUN git clone https://github.com/zykon2004/c2-server-cli.git /c2-server-cli

WORKDIR /c2-server-cli
RUN pip install --no-cache-dir --upgrade -r /c2-server-cli/requirements.txt


EXPOSE 8080-8080

CMD ["python", "/c2-server/server/server.py"]
