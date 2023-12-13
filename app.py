import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, render_template_string, request, redirect, abort

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'secret_key',
    'SQLALCHEMY_DATABASE_URI': f'sqlite:///{basedir}/app.db',
})
db = SQLAlchemy(app)
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(120), index=True, nullable=False)
    status = db.Column(db.Boolean, default=False)
with app.app_context(): db.create_all()

@app.errorhandler(404)
def page_not_found(error):
    return f'{error.description}', 404

@app.route('/')
@app.route('/index')
def index():
    entries = Entry.query.all()
    return render_template_string(
        """
        <form action="/add" method="post">
            <input type="text" name="title">
            <textarea name="description"></textarea>
            <button type="submit">Add</button>
        </form>
        {% for entry in entries %}
            {{ entry.id }}.{{ entry.title }}({{ entry.status }}):{{ entry.description }}
            <a href="/turn/{{ entry.id }}">Toggle</a>
            <a href="/delete/{{ entry.id }}">Delete</a>
            <a href="/update/{{ entry.id }}">Edit</a>
            <br/>
        {% endfor %}
        """,
        entries=entries
    )

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        form = request.form
        title = form.get('title')
        description = form.get('description')
        if not title or description:
            entry = Entry(title = title, description = description)
            db.session.add(entry)
            db.session.commit()
            return redirect('/')
    return "Never give up"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    entry = db.session.get(Entry, id)
    if not entry: return abort(404, description="Cannot get Entry")
    if request.method == 'POST':
        form = request.form
        title = form.get('title')
        description = form.get('description')
        entry.title = title
        entry.description = description
        db.session.commit()
        return redirect('/')
    return render_template_string(
        """
        <form action="/update/{{ entry.id }}" method="post">
            <input type="text" name="title" value="{{ entry.title }}">
            <textarea name="description">{{ entry.description }}</textarea>
            <button type="submit">Update</button>
        </form>
        """,
        entry = entry
    )

@app.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        entry = db.session.get(Entry, id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/')
    return "Never give up"

@app.route('/turn/<int:id>')
def turn(id):
    if not id or id != 0:
        entry = db.session.get(Entry, id)
        if entry:
            entry.status = not entry.status
            db.session.commit()
        return redirect('/')
    return "Never give up"

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 5000, debug=True)
