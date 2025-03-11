from sqlalchemy import create_engine, String, Column, Integer
from sqlalchemy.orm import sessionmaker, DeclarativeBase, registry

# This is where I define the engine string... this is a temp, will have to loaded from settings
engine = create_engine('sqlite:///database.db')

Session = sessionmaker(bind=engine)
session = Session()

reg = registry()

# This is the basics we need to make a class
class Base(DeclarativeBase):
  registry = reg

# The actual script database
class Script()
  __tablename__ = 'scripts'
  
  script_id = Column(String, primary_key=True)
  script_content = Column(String)
  script_string = Column(String)

def create_script():
  pass

def update_script():
  pass

def delete_script():
  pass
