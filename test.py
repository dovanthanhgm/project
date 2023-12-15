import os
from flask import Flask, request, jsonify, make_response, Blueprint
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.update({'SECRET_KEY': 'secret_key','SQLALCHEMY_DATABASE_URI': f'sqlite:///{basedir}/app.db'})
db = SQLAlchemy(app)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    def json(self): return {'id': self.id, 'title': self.title}
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
        product = Product(title=data['title'])
        db.session.add(product)
        db.session.commit()
        return make_response(jsonify({'message': 'success'}), 201)
    return 'Something went wrong'
app.register_blueprint(api, url_prefix='/api')
##################################################
from flask import render_template_string
shop = Blueprint('shop', __name__)
@shop.route('/home')
def index():
    products = Product.query.all()
    return render_template_string(
        """
        <!DOCTYPE html><html><head>
        <style>
            table, th, td {border-collapse: collapse;border: 1px solid black;}
        </style>
        </head>
        <body>
            <table><thead><tr>
                <th>ID</th>
                <th>Title</th>
                <th>Description</th>
            </tr></thead><tbody>
                {% for product in products %}
                <tr>
                    <td>{{ product.id }}</td>
                    <td>{{ product.title }}</td>
                    <td> Lorem ipsum. </td>
                </tr>
                {% endfor %}
            </tbody></table>
        </body></html>
        """,
        products=products
    )
app.register_blueprint(shop, url_prefix='/shop')
##################################################
from flask import render_template_string
shop_v2 = Blueprint('shop_v2', __name__)
@shop_v2.route('/home')
def index():
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