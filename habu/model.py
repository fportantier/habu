import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy_utils import ChoiceType, IPAddressType, ArrowType

HOME = os.path.expanduser('~')
DBFILE = 'sqlite:///' + HOME + '/habu.sqlite'

print(DBFILE)

engine = create_engine(DBFILE)
Base = declarative_base()

class Port(Base):
    __tablename__ = 'ports'

    id = Column(Integer, primary_key=True)
    ip = Column(IPAddressType())
    number = Column(Integer)
    protocol = Column(Enum('tcp', 'udp', 'sctp', name='port_protocols'))
    updated = Column(ArrowType())

#Base.metadata.create_all(engine)


