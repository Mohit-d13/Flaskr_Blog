import sqlite3
from datetime import datetime

import click
from flask import current_app, g
# for connecting to database performing queries and operations, open and close the connection 


def get_db():
    # call for handling request, outside flaskr file
    if 'db' not in g:
    # g is special object to store data for multiple request    
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            # for using current app to handle request
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        # return row data to behave like dicts
        
    return g.db


def close_db(e=None):
    # close connection if connection exits
    db = g.pop('db', None)
    
    if db is not None:
        db.close()


def init_db():
    # open sql file read and decode its commands
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    

#define commands to call init_db function    
@click.command('init-db')
def init_db_command():
    # Clear the existing data and create a new tables.
    init_db()
    click.echo('Initialized the database.')
    
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)


def init_app(app):
    app.teardown_appcontext(close_db)
    # tells Flask to call the function when cleaning up after returning the response.
    app.cli.add_command(init_db_command)
    # adds a new command that can be called with flask command.
    