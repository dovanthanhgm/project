import os
from datetime import datetime
from flask import Flask, request, jsonify, make_response, Blueprint
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.update({'SECRET_KEY': 'secret_key','SQLALCHEMY_DATABASE_URI': f'sqlite:///{basedir}/app.db'})
db = SQLAlchemy(app)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def json(self): return {'id': self.id, 'title': self.title, 'description': self.description, 'image': self.image, 'created_at': self.created_at}
with app.app_context(): db.create_all()
##################################################
api = Blueprint('api', __name__)
@api.route('/list', methods=['GET'])
def list():
    products = Product.query.all()
    if products: return make_response(jsonify([product.json() for product in products]), 200)
    return 'Something went wrong'
@api.route('/add', methods=['POST'])
def add():
    try: data = request.get_json()
    except: data = request.form
    if data:
        product = Product(title=data['title'], description=data['description'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        return make_response(jsonify({'message': 'success'}), 201)
    return 'Something went wrong'
app.register_blueprint(api, url_prefix='/api')
##################################################
from flask import render_template_string
shop = Blueprint('shop', __name__)
@shop.route('/home')
def home():
    products = Product.query.all()
    return render_template_string(
        """
        <!DOCTYPE html><html><head>
        <style>
            body {width: 75%; margin: 1rem auto; border-collapse: collapse; border: 1px solid black;} ul, li {list-style-type: none} li {display: inline-block; margin-right: 10px;} table, ul {width: 90%; margin: 1rem auto} table, th, td {border-collapse: collapse;border: 1px solid black;}
            
        </style>
        </head>
        <body>
            <ul>
                <li><a href="{{ url_for('shop.home') }}">Home</a></li>
                <li><a href="{{ url_for('shop.add') }}">Add</a></li>
            </ul> <hr>
            <table><thead><tr>
                <th>ID</th>
                <th>Title</th>
                <th>Description</th>
                <th>Image</th>
                <th>CreatedAt</th>
            </tr></thead><tbody>
                {% for product in products %}
                <tr>
                    <td>{{ product.id }}</td>
                    <td>{{ product.title }}</td>
                    <td> {{ product.description }} </td>
                    <td> <img src="{{ product.image }}" style="width: 50px; height: 50xp;"/> </td>
                    <td> {{ product.created_at.strftime("%d/%m/%Y") }} </td>
                </tr>
                {% endfor %}
            </tbody></table>
        </body></html>
        """,
        products=products
    )
@shop.route('/add')
def add():
    return render_template_string(
        """
        <!DOCTYPE html><html><head>
        <style>
        </style>
        </head>
        <body>
            <form>
                <input type="text">
            </form>
        </body></html>
        """,
    )
app.register_blueprint(shop, url_prefix='/shop')
##################################################
from flask import render_template_string
shop_v2 = Blueprint('shop_v2', __name__)
@shop_v2.route('/home')
def home():
    products = Product.query.all()
    return render_template_string(
        """
        <!DOCTYPE html><html><head>
        <style>
            table, th, td {border-collapse: collapse;border: 1px solid black;}
        </style>
        <script>
        document.addEventListener("DOMContentLoaded", function () {
            fetch('https://psychic-umbrella-r44496q5w6rjcpx9g-5000.app.github.dev/api/list')
                .then(response => response.json())
                .then(data => {
                    res_string = JSON.stringify(data);
                    res_data = JSON.parse(res_string)
                    console.log(data);
                    document.getElementById("content").innerHTML += `
                        <tr>
                            <td>1</td>
                            <td>${data[0].title}</td>
                            <td>${data[0].description}</td>
                        </tr>
                    `;
                })
        });
        </script>
        </head>
        <body>
            <table><thead><tr>
                <th>ID</th>
                <th>Title</th>
                <th>Description</th>
            </tr></thead><tbody id="content">
            </tbody></table>
        </body></html>
        """,
        products=products
    )
app.register_blueprint(shop_v2, url_prefix='/shop_v2')
##################################################
@app.route('/', methods=['GET'])
def hello(): return 'hello'
if __name__ == '__main__': app.run(host = '0.0.0.0', port = 5000, debug=True)