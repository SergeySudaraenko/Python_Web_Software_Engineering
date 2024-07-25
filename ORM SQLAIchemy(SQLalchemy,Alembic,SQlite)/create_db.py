from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from models import Base

engine = create_engine('sqlite:///database.db')


Base.metadata.create_all(engine)
    


