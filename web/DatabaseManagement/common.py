from sqlalchemy import create_engine, String, Column, Integer, exc
from sqlalchemy.orm import sessionmaker, DeclarativeBase, registry

# This is where I define engine string... this is a temp, will have it loaded from settings
engine = create_engine('sqlite:///database.db')

Session = sessionmaker(bind=engine)
session = Session()

reg = registry()

# This is the basics we need to make a class
class Base(DeclarativeBase):
  registry = reg

Base.metadata.create_all(engine)

def all_find_record(record_type):
  try:
    record = session.query(record_type).all()
  except exc.OperationalError:
    return [record_type()]
  return record

def find_record(record_type, **matcher):
  try:
    record = session.query(record_type).filter_by(**matcher).first()
  except exc.OperationalError:
    return record_type()
  return record

def create_record(record_type, **record_data):
  record = record_type(**record_data)
  session.add_all([record])
  session.commit()
  return record

def delete_record(record):
  session.delete(record)
  session.commit()
 
def update_fields(record, **fields):
  for key, value in fields.items():
    setattr(record, key, value)
  session.commit()
  return True
