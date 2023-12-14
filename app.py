import os
from flask import Flask
from models import db
from test_app import test_app
from api import api

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.update({'SECRET_KEY': 'secret_key','SQLALCHEMY_DATABASE_URI': f'sqlite:///{basedir}/app.db'})
db.init_app(app)
with app.app_context(): db.create_all()

app.register_blueprint(test_app, url_prefix='/test_app')
app.register_blueprint(api, url_prefix='/api')

@app.route('/', methods=['GET'])
def hello(): return 'hello'

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 5000, debug=True)
