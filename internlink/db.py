from flask import Flask, g
import MySQLdb

connection_params = {}

def init_db(app: Flask, user: str, password: str, host: str, database: str, port: int = 3306, autocommit: bool = True):
    connection_params['user'] = user
    connection_params['password'] = password
    connection_params['host'] = host
    connection_params['database'] = database
    connection_params['port'] = port
    connection_params['autocommit'] = autocommit
    app.teardown_appcontext(close_db)

def get_db():
    if 'db' not in g:
        g.db = MySQLdb.connect(**connection_params)
    return g.db

def get_cursor():
    return get_db().cursor(cursorclass=MySQLdb.cursors.DictCursor)

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
