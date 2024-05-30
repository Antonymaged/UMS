from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///data/university.db', echo=False)
base = declarative_base()
class University(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    passw = Column(String, nullable=False)
    email = Column(String, nullable=False)
    def __init__(self, nam, passw, email):
        self.name = nam
        self.passw = passw
        self.email = email

base.metadata.create_all(engine)