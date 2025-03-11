from sqlalchemy import create_engine, String, Column, Integer
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

def all_find_record(record_type, matcher):
  matcher = {matcher: matcher}
  record = session.query(record_type).filter_by(**matcher).all()
  return record

def first_find_record(record_type, matcher):
  record = all_find_record(record_type, matcher)
  if len(record) >= 0:
    record = record[0]
  return record

def update_fields(record, **fields):
  for key, value in fields.items():
    setattr(record, key, value)
  session.commit()
