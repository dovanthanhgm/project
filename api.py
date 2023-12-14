from flask import request, Blueprint, jsonify, make_response
from models import db, Poll

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
