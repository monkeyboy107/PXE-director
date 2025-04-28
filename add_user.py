from web.DatabaseManagement import UserManagement
import argparse
import random

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
         'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B',
         'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
         'G', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4',
         '5', '6', '7', '8', '9', '0']

password = ''
password_size = 8

for i in range(password_size) : password = password + random.choice(chars)

parser = argparse.ArgumentParser(
  prog='AddUser',
  description='Backup utility in case you delete all your users or otherwise loose access'
  )
  
# Adds the arguments
parser.add_argument('username', help='The user you want to add')
parser.add_argument('-p', '--password', nargs=1, help='Overwrite the random password and set your own')
parser.add_argument('-r', '--password-reset', action='store_true', help='Resets password for specified user')

# Parse scan
args = parser.parse_args()

if args.password:
  print('Ovewriting password')
  password = args.password[0]

if args.password_reset:
  UserManagement.reset_password(args.username, password)
  print(f'Congradulations! The user has been updated! The username is {args.username}, {password} is the password. When you get signed in. You will need to reset your password.')
else:
  result = UserManagement.add_user(args.username, password)
  if result:
    print(f'Congradulations! The user has been created! The username is {args.username}, {password} is the password. When you get signed in. You will need to reset your password.')
  else:
    print('Error! User already exists')
