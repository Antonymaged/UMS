from sqlalchemy import create_engine, Integer, Double, String, Column
from sqlalchemy.orm import declarative_base

def m(n):
    n   
    global engine,base
    engine = create_engine('sqlite:///data/{}.db'.format(n), echo=False)
    base = declarative_base()

    class University(base):
        __tablename__ = "students"
        stu_id = Column(Integer, primary_key=True)
        stu_name = Column(String, nullable=False)
        stu_fac = Column(String, nullable=False)
        stu_lev = Column(Integer, nullable=False)
        stu_age = Column(Integer, nullable=False)
        stu_gpa = Column(Double, nullable=False)
        stu_numcor = Column(Integer, nullable=False)
    
    def __init__(self, name):
        self.n = name

    base.metadata.create_all(engine)