from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    def json(self): return {'id': self.id, 'title': self.title}
