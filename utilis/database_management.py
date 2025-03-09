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

# The actual user class. This is the most important for this
class User(Base):
  __tablename__ = 'users'

  name = Column(String, primary_key=True)
  password = Column(String)

Base.metadata.create_all(engine)

def add_user(username, password):
  if [] == find_user(username):
    user = User(name=username, password=password)
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

if '__main__' == __name__: 
  add_user('Test user', '12345abcde')
  find_user('Test user')
  delete_user('Nonexsist')
  delete_user('Test user')
