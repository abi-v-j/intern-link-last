from collections import namedtuple
from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
flask_bcrypt = Bcrypt(app)

UserAccount = namedtuple('UserAccount', ['username', 'password'])

users = [
    UserAccount('user1', 'password123'),
    UserAccount('user2', 'password456'),
    UserAccount('staff1', 'staffpass123'),
    UserAccount('staff2', 'staffpass456'),
    UserAccount('admin1', 'adminpass123')
]

for user in users:
    password_hash = flask_bcrypt.generate_password_hash(user.password).decode('utf-8')
    is_valid = flask_bcrypt.check_password_hash(password_hash, user.password)
    print(f'Username: {user.username}')
    print(f'Password: {user.password}')
    print(f'Hash: {password_hash}')
    print(f'Verified: {is_valid}')
    print()
