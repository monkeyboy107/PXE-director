from flask import session

def login_check():
  if 'username' in session:
    if session.get('username', None):
      return True
  return False


