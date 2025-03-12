from sqlalchemy import create_engine, String, Column, Integer
from sqlalchemy.orm import sessionmaker, DeclarativeBase, registry
from argon2 import PasswordHasher
from DatabaseManagement import common 

session = common.session
Base = common.Base

# The actual user class. This is the most important for this
class User(Base):
  __tablename__ = 'users'

  username = Column(String, primary_key=True)
  display_name = Column(String)
  nickname = Column(String)
  email = Column(String)
  password = Column(String)


def add_user(username, password):
  if None == find_user(username):
    password_hash = hash_password(password)
    common.create_record(User, username=username, password=password)
    return True
  else:
    return False

def delete_user(username):
  user = find_user(username)
  if user == None:
    return False
  else: 
    common.delete_record(user)
    return User

def find_user(username):
  user = common.find_record(User, username=username)
  return user

def find_all_users():
  users = common.all_find_record(User)
  return users

def reset_password(username, password):
  password = hash_password(password)
  update_field(username, password=password)
  
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

def update_field(username, **user_fields):
  user = find_user(username)
  common.update_fields(user, **user_fields)

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
