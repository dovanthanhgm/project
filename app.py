import os
from flask import Flask, render_template_string, request, redirect, abort, jsonify, make_response, Blueprint, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.update({'SECRET_KEY': 'secret_key','SQLALCHEMY_DATABASE_URI': f'sqlite:///{basedir}/app.db'})
db = SQLAlchemy(app)
class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    def json(self): return {'id': self.id, 'title': self.title}
with app.app_context(): db.create_all()

test_app = Blueprint('test_app', __name__)
@test_app.route('/add', methods=['POST'])
def add():
    try:
        poll = Poll(title = request.form['title'])
        db.session.add(poll)
        db.session.commit()
        return redirect(url_for('test_app.list'))
    except: return 'Something went wrong'
@test_app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    poll = db.session.get(Poll, id)
    if not poll: return abort(404, description="Cannot get poll")
    if request.method == 'POST':
        poll.title = request.form['title']
        db.session.commit()
        return redirect(url_for('test_app.list'))
    return render_template_string("""<form action="{{url_for('test_app.update',id=poll.id)}}" method="post"><input type="text" name="title" value="{{poll.title}}"><button type="submit">Update</button></form>""",poll=poll)
@test_app.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        poll = db.session.get(Poll, id)
        if poll:
            db.session.delete(poll)
            db.session.commit()
        return redirect(url_for('test_app.list'))
    return 'Something went wrong'
@test_app.route('/list')
def list():
    polls = Poll.query.all()
    return render_template_string("""<form action="{{ url_for('test_app.add') }}" method="post"><input type="text" name="title"><button type="submit">Add</button></form>{% for poll in polls %}{{ poll.title }}<a href="{{ url_for('test_app.delete', id=poll.id) }}">Delete</a><a href="{{ url_for('test_app.update', id=poll.id) }}">Edit</a><br/>{% endfor %}""",polls=polls)
@test_app.errorhandler(404)
def page_not_found(error):
    return f'{error.description}', 404
app.register_blueprint(test_app, url_prefix='/test_app')

api = Blueprint('api', __name__)
@api.route('/list', methods=['GET'])
def list():
    polls = Poll.query.all()
    if polls: return make_response(jsonify([poll.json() for poll in polls]), 200)
    return 'Something went wrong'
@api.route('/add', methods=['POST'])
def add():
    try: data = request.get_json()
    except: data = request.form
    if data:
        poll = Poll(title=data['title'])
        db.session.add(poll)
        db.session.commit()
        return make_response(jsonify({'message': 'success'}), 201)
    return 'Something went wrong'
app.register_blueprint(api, url_prefix='/api')

@app.route('/', methods=['GET'])
def hello(): return 'hello'

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 5000, debug=True)
