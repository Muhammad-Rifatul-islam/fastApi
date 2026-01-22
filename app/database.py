from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Database_url="postgresql://postgres:5112@localhost/python-fast-api"
engine=create_engine(Database_url)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
     db=SessionLocal()
   
     try:
          yield db

     finally:
          db.close()      
