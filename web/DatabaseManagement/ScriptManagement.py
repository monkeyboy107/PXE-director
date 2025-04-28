from sqlalchemy import create_engine, String, Column, Integer
from sqlalchemy.orm import sessionmaker, DeclarativeBase, registry
from DatabaseManagement import common

session = common.session
Base = common.Base

# The actual script database
class Script(Base):
  __tablename__ = 'scripts'
  
  id = Column(String, primary_key=True)
  content = Column(String)
  descrpition = Column(String)

def create_script(id, content, description):
  common.create_record(Script, id=id, content=content, description=description)

def update_script(**field):
  common.update_record(Script, **field)

def delete_script(id):
  script = find_script(id)
  commmon.delete_record(script)

def find_script(id):
  script = common.find_record(Script, id)
  return script

def find_all_scripts():
  scripts = common.all_find_record(Script)
  return scripts
