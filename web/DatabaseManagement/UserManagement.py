from sqlalchemy import create_engine, String, Column, Integer
from sqlalchemy.orm import sessionmaker, DeclarativeBase, registry
from argon2 import PasswordHasher
import random

# This is where I define engine string... this is a temp, will have it loaded from settings 
engine = create_engine('sqlite:///database.db')

Session = sessionmaker(bind=engine)
session = Session()

reg = registry()

# This is the basics we need to make a class
class Base(DeclarativeBase):
  registry = reg

# The actual user class. This is the most important for this
class User(Base):
  __tablename__ = 'users'

  name = Column(String, primary_key=True)
  password = Column(String)

Base.metadata.create_all(engine)

def add_user(username, password):
  if None == find_user(username):
    password_hash = hash_password(password)
    user = User(name=username, password=password_hash)
    session.add_all([user])
    session.commit()
    return True
  else:
    return False

def delete_user(username):
  user = find_user(username)
  if user == None:
    return False
  else: 
    session.delete(user)
    session.commit()
    return User

def find_user(username):
  user = session.query(User).filter_by(name=username).first()
  return user

def reset_password(username, password):
  user = find_user(username)
  password = hash_password(password)
  user.password = password
  session.commit()

def hash_password(password):
  ph = PasswordHasher()
  hash = ph.hash(password)
  return hash

def test_authentication(username, password):
  user = find_user(username)
  ph = PasswordHasher()
  result = False
  try:
    result = ph.verify(user.password, password)
  except Exception as e:
    print(f'Failed to authenticate: {e}')
  return result

if '__main__' == __name__: 
  delete_user('Test user')
  add_user('Test user', '12345abcde')
  if test_authentication('Test user', '12345abcde'):
    print('Successful login!')
  else:
    print('Unsuccesful login...')
  if test_authentication('Test user', 'incorrect password'):
    print('Succesful login...')
  else:
    print('Unsuccesful login!')
