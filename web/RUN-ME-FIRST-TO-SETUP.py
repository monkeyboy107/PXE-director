import generate_SSL_cert
import common_tools
import argparse

description = 'You should run this first. You can rerun this in case something breaks too'

parser = argparse.ArgumentParser(description=description)
parser.add_argument('--new-user', help='This will add a new user through CLI. Requires --user-password')
parser.add_argument('--user-password', help='This will add a new user password through CLI. Requires --user-password')
parser.add_argument('--regen-ssl', help='This will regenerate SSL key and cert')


args = parser.parse_args()
none_count = 0

# This checks if the parser is being used
if args.regen_ssl is not None:
    generate_SSL_cert.cert_gen()
else:
    none_count = none_count + 1
if args.new_user is not None and args.user_password is not None:
    common_tools.add_user(args.new_user, args.user_password, '', 'sha512')
elif args.new_user is not None or args.user_password is not None:
    print('requies both --new-user and --user-password')
else:
    none_count = none_count + 1

# If the parser is not being used then it will go through first run setup
if none_count == 2:
    print('Welcome to PXE-director.')
    username = input('Please put in a username! ')
    password = input('Please put in a password! ')
    common_tools.add_user(username, password, '', 'sha512')
    print('Please note if you run into trouble you can rerun this like the following '
          '\'python3 RUN-ME-FIRST-TO-SETUP.py --username USERNAME --password PASSWORD\'')
    generate_SSL_cert.cert_gen()
    print('If you need to regenerate your SSL cert please run the following '
          '\'python --regen-ssl RUN-ME-FIRST-TO-SETUP.py regen\'')
