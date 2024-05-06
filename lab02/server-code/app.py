from flask import Flask, jsonify, abort, request, send_from_directory, send_file
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']
app.config['UPLOAD_PATH'] = '../images'
products = []
base_dir = os.path.abspath(os.path.dirname(__file__))

def search_by_id(product_id):
    product = None
    for t in products:
        if t['id'] == product_id:
            product = t
    if product == None:
        abort(404)
    return product

@app.route('/product', methods=['POST'])
def create_product():
    if not request.json or not 'name' or not 'description' in request.json:
        abort(400)
    if type(request.json['name']) != str:
        abort(400)
    if type(request.json['description']) != str:
        abort(400)
    generated_id = 0 if not len(products) else products[-1]['id'] + 1

    product = {
        'id': generated_id,
        'name': request.json['name'],
        'description': request.json['description'], 
        'icon': ''
    }
    products.append(product)
    return jsonify(product), 201

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    for product in products:
        if product['id'] == product_id:
            return jsonify(product), 200
    abort(404)

@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = search_by_id(product_id)
        
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) != str:
        abort(400)
    product['name'] = request.json.get('name', product['name'])
    product['description'] = request.json.get('description', product['description'])
    return jsonify(product), 200

@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    for product in products:
        if product['id'] == product_id:
            products.remove(product)
            return jsonify(product), 200
    abort(404)
    

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products), 200


@app.route('/product/<int:product_id>/image', methods=['POST'])
def upload_image(product_id):
    product = search_by_id(product_id)

    if 'icon' not in request.files:
        return 'No file part', 400
    uploaded_file = request.files['icon']
    if uploaded_file.filename == '':
        return 'No selected file', 400
    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            uploaded_file.save(os.path.join(base_dir, app.config['UPLOAD_PATH'], filename))
            product['icon'] = str(filename)

    return jsonify(product), 200

@app.route('/product/<int:product_id>/image', methods=['GET'])
def get_image(product_id):
    product = search_by_id(product_id)
    if product['icon'] == '':
        return 'No icon for this product', 404
    return send_file(os.path.join(app.config['UPLOAD_PATH'], product['icon']))


if __name__ == '__main__':
    app.run(debug=True)