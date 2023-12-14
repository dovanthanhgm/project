from flask import render_template_string, request, redirect, abort, Blueprint, url_for
from models import db, Poll

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
