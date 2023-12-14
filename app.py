import os
from flask import Flask, render_template_string, request, redirect, abort, jsonify, make_response, Blueprint, url_for
from flask_sqlalchemy import SQLAlchemy

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
    def json(self):
        return {'id': self.id,'title': self.title, 'description': self.description, 'status': self.status}
with app.app_context(): db.create_all()
##############################
# Test App
test_app = Blueprint('test_app', __name__)
@test_app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        form = request.form
        title = form.get('title')
        description = form.get('description')
        if not title or description:
            entry = Entry(title = title, description = description)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('test_app.index'))
    return 'Something went wrong'
@test_app.route('/update/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('test_app.index'))
    return render_template_string(
        """
        <form action="{{ url_for('test_app.update', id=entry.id) }}" method="post">
            <input type="text" name="title" value="{{ entry.title }}">
            <textarea name="description">{{ entry.description }}</textarea>
            <button type="submit">Update</button>
        </form>
        """,
        entry = entry
    )
@test_app.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        entry = db.session.get(Entry, id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect(url_for('test_app.index'))
    return 'Something went wrong'
@test_app.route('/turn/<int:id>')
def turn(id):
    if not id or id != 0:
        entry = db.session.get(Entry, id)
        if entry:
            entry.status = not entry.status
            db.session.commit()
        return redirect(url_for('test_app.index'))
    return 'Something went wrong'
@test_app.route('/')
def index():
    entries = Entry.query.all()
    return render_template_string(
        """
        <form action="{{ url_for('test_app.add') }}" method="post">
            <input type="text" name="title">
            <textarea name="description"></textarea>
            <button type="submit">Add</button>
        </form>
        {% for entry in entries %}
            {{ entry.id }}.{{ entry.title }}({{ entry.status }}):{{ entry.description }}
            <a href="{{ url_for('test_app.turn', id=entry.id) }}">Toggle</a>
            <a href="{{ url_for('test_app.delete', id=entry.id) }}">Delete</a>
            <a href="{{ url_for('test_app.update', id=entry.id) }}">Edit</a>
            <br/>
        {% endfor %}
        """,
        entries=entries
    )
@test_app.errorhandler(404)
def page_not_found(error):
    return f'{error.description}', 404
app.register_blueprint(test_app, url_prefix='/test_app')
##############################
# API
api = Blueprint('api', __name__)
@api.route('/list', methods=['GET'])
def list():
    entries = Entry.query.all()
    if entries:
        return make_response(jsonify([entry.json() for entry in entries]), 200)
    return 'Something went wrong'
@api.route('/add', methods=['POST'])
def add():
    try: data = request.get_json()
    except: data = request.form
    if data:
        entry = Entry(title=data['title'], description=data['description'])
        db.session.add(entry)
        db.session.commit()
        return make_response(jsonify({'message': 'success'}), 201)
    return 'Something went wrong'
app.register_blueprint(api, url_prefix='/api')
##############################

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 5000, debug=True)
