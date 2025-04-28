from sqlalchemy import create_engine, String, Column, Integer
from sqlalchemy.orm import sessionmaker, DeclarativeBase, registry

engine = create_engine('sqlite:///database.db')

Session = sessionmaker(bind=engine)
session = Session()

reg = registry()

class Base(DeclarativeBase):
  registry = reg

class User(Base):
  __tablename__ = 'users'

  username = Column(String, primary_key=True)
  display_name = Column(String)
  nickname = Column(String)
  email = Column(String)
  password = Column(String)

Base.metadata.create_all(engine)

users = session.query(User).all()

for user in users:
  print(f'The user is {user.username} the hash is {user.password} and display name of {user.display_name}')
