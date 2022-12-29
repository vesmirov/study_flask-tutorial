import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth/')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('auth.login'))
        return view
    return wrapped_view()


# bp.route associates the URL /register with the register view
@bp.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # form - a dict mapping object
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # simple validation
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'

        if not error:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f'User {username} is already registered'
            else:
                return redirect(url_for('auth.login'))

        # flash stores messages that can be retrieved when rendering the template
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # fetchone returns one row from the query, or None if no query returned
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if not user:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if not error:
            # session - a dict, which stores data across requests
            session.clear()
            # since the validation succeeds, the user id is stored in a new session
            # the data is stored in a cookie that is sent to the browser
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))


# before_app_request - registers a function that runs before the view function (in any case)
@bp.before_app_request
def load_logged_in_user():
    """checks if a user id is stored in the session and gets that data from the database """

    user_id = session.get('user_id')

    if not user_id:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
