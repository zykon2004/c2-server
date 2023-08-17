from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase  # type: ignore


class Base(DeclarativeBase):
    ...


class Client(Base):
    __tablename__ = "clients"

    id = Column(String, primary_key=True, nullable=False)
    hostname = Column(String)
    os = Column(String)
    last_seen = Column(DateTime)
    port = Column(Integer)
    external_ip = Column(String)


class Payload(Base):
    __tablename__ = "payloads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    payload = Column(Text)
    default_arguments = Column(Text)


class Command(Base):
    __tablename__ = "commands"

    id = Column(String, primary_key=True, nullable=False)
    payload_id = Column(Integer, ForeignKey("payloads.id"))
    arguments = Column(Text)
    client_id = Column(String, ForeignKey("clients.id"))
    time_sent = Column(DateTime)
    status = Column(Integer)
    response = Column(Text)
    type = Column(Integer)
    last_update = Column(DateTime)
