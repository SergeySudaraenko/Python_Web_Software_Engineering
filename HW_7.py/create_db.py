from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models import Base


engine = create_engine('sqlite:///your_database.db')



print("Successfully.")
