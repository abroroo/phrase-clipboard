from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    phrases = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM phrases p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', phrases=phrases, include_js=True)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO phrases (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_phrase(id, check_author=True):
    phrase = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM phrases p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if phrase is None:
        abort(404, f"phrase id {id} doesn't exist.")

    if check_author and phrase['author_id'] != g.user['id']:
        abort(403)

    return phrase


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    phrase = get_phrase(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE phrases SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', phrase=phrase)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_phrase(id)
    db = get_db()
    db.execute('DELETE FROM phrases WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))