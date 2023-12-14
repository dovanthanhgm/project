import os
from flask import Flask, request, jsonify, make_response
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

@app.route('/', methods=['GET'])
def hello(): return 'hello'

@app.route('/list', methods=['GET'])
def list():
    polls = Poll.query.all()
    if polls: return make_response(jsonify([poll.json() for poll in polls]), 200)
    return 'Something went wrong'

@app.route('/add', methods=['POST'])
def add():
    try: data = request.get_json()
    except: data = request.form
    if data:
        poll = Poll(title=data['title'])
        db.session.add(poll)
        db.session.commit()
        return make_response(jsonify({'message': 'success'}), 201)
    return 'Something went wrong'

if __name__ == '__main__': app.run(host = '0.0.0.0', port = 5000, debug=True)
