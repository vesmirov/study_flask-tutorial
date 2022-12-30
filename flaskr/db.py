import sqlite3

import click
from flask import current_app, g


def get_db():
    """
    the connection is stored and reused instead of creating a new one
    if ged_db is called for the second time for the same request
    """
    if 'db' not in g:
        # 'g' is used to store data that might be accessed by multiple functions during the request
        g.db = sqlite3.connect(
            # points tp the Flask application handling the request
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        # tells the connection to return rows that behave like dicts (allows accessing the columns by name)
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    db = get_db()

    # open_resource opens a file relative to the flaskr package
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def close_db(e=None):
    """checks if a connection was created by checking if g.db was set."""

    db = g.pop('db', None)

    if db is not None:
        db.close()


# '@click.command' defines a command line command called init-db that calls the db function
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables"""

    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register the functions with the application instance"""

    # tells Flask to call the function when cleaning up after returning the response
    app.teardown_appcontext(close_db)

    # adds a new command that can be called with the flask command
    app.cli.add_command(init_db_command)
