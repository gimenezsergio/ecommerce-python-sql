import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, Product

# Cargar las variables de entorno desde el archivo .env si existe
load_dotenv()

# Inicializamos la aplicación Flask indicando que los archivos estáticos (HTML/JS/CSS) están en la raíz del proyecto
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__, static_folder=PROJECT_ROOT, static_url_path='')

# Habilitamos CORS para permitir peticiones desde el cliente web
CORS(app)

# Ruta principal para servir el archivo index.html del Frontend
@app.route('/')
def serve_index():
    return app.send_static_file('index.html')


# Configuración de la Base de Datos SQL leída dinámicamente desde .env
# Si no está definida en .env, usa SQLite local por defecto como respaldo (fallback)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
default_db_path = 'sqlite:///' + os.path.join(BASE_DIR, 'ecommerce.db')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', default_db_path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Vinculamos la instancia de SQLAlchemy con nuestra app de Flask
db.init_app(app)


# Endpoint de comprobación de estado (Health Check)
@app.route('/api/health', methods=['GET'])
def health_check():
    """Ruta simple para verificar que el servidor API está vivo y respondiendo."""
    return jsonify({
        'status': 'ok',
        'message': 'Backend de Ecommerce en Flask funcionando correctamente'
    })

# Endpoint que entrega la configuración pública (leída desde .env) al Frontend
@app.route('/api/config', methods=['GET'])
def get_config():
    """
    Entrega variables públicas del entorno (.env) al cliente JS.
    Permite que el frontend configure su BASE_URL dinámicamente según el servidor.
    """
    api_url = os.getenv('API_BASE_URL', 'http://localhost:5000/api')
    return jsonify({
        'apiUrl': api_url
    }), 200


# Endpoint para obtener el listado de productos desde la base de datos SQL
@app.route('/api/products', methods=['GET'])
def get_products():
    """
    Retorna la lista de productos de la base de datos SQL.
    Soporta los parámetros de consulta (query params):
    - sort: 'asc' o 'desc' (ordenar por ID)
    - limit: número entero para limitar la cantidad de resultados
    """
    from flask import request

    # Iniciamos la consulta base sobre la tabla 'products' usando SQLAlchemy
    query = Product.query

    # 1. Aplicar ordenamiento si se pasa el parámetro 'sort'
    sort_param = request.args.get('sort')
    if sort_param == 'desc':
        query = query.order_by(Product.id.desc())
    elif sort_param == 'asc':
        query = query.order_by(Product.id.asc())

    # 2. Aplicar límite si se pasa el parámetro 'limit'
    limit_param = request.args.get('limit')
    if limit_param and limit_param.isdigit():
        query = query.limit(int(limit_param))

    # Ejecutamos la consulta SQL (SELECT * FROM products ...)
    products = query.all()

    # Convertimos cada objeto de producto SQL a un diccionario usando .to_dict()
    products_json = [p.to_dict() for p in products]

    # Retornamos el array en formato JSON con código HTTP 200 OK
    return jsonify(products_json), 200

# Endpoint para obtener el detalle de un producto por su ID
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_detail(product_id):
    """
    Retorna los datos de un único producto buscando por su clave primaria (ID) en la DB SQL.
    - Si el producto existe: devuelve el JSON con código 200 OK.
    - Si no existe: devuelve un mensaje de error en JSON con código HTTP 404 Not Found.
    """
    # db.session.get(Product, product_id) es el método moderno de SQLAlchemy 2.0 para buscar por ID
    product = db.session.get(Product, product_id)

    # Verificamos si la consulta SQL devolvió un registro
    if not product:
        return jsonify({'message': f'Producto con ID {product_id} no encontrado'}), 404

    # Devolvemos el producto en formato JSON
    return jsonify(product.to_dict()), 200

# Endpoint para obtener la lista de categorías únicas de productos
@app.route('/api/products/categories', methods=['GET'])
def get_categories():
    """
    Retorna la lista de categorías únicas presentes en la base de datos SQL.
    Equivale a la consulta SQL: SELECT DISTINCT category FROM products;
    """
    # db.session.query(Product.category).distinct().all() ejecuta la consulta SQL DISTINCT
    categories_query = db.session.query(Product.category).distinct().all()

    # Extraemos el primer elemento de cada tupla obtenida [(cat1,), (cat2,)...]
    categories_list = [item[0] for item in categories_query if item[0]]

    # Devolvemos el array de strings en formato JSON
    return jsonify(categories_list), 200

# Endpoint para obtener productos filtrados por una categoría específica
@app.route('/api/products/category/<string:category_name>', methods=['GET'])
def get_products_by_category(category_name):
    """
    Retorna todos los productos que pertenecen a la categoría especificada.
    Equivale a la consulta SQL: SELECT * FROM products WHERE category = category_name;
    Soporta también los query params sort y limit.
    """
    from flask import request

    # Consulta base filtrando por categoría
    query = Product.query.filter_by(category=category_name)

    # Ordenamiento
    sort_param = request.args.get('sort')
    if sort_param == 'desc':
        query = query.order_by(Product.id.desc())
    elif sort_param == 'asc':
        query = query.order_by(Product.id.asc())

    # Límite
    limit_param = request.args.get('limit')
    if limit_param and limit_param.isdigit():
        query = query.limit(int(limit_param))

    products = query.all()
    products_json = [p.to_dict() for p in products]

    return jsonify(products_json), 200

if __name__ == '__main__':


    # Leemos el puerto y el modo debug desde las variables de entorno (.env)
    # Convertimos el puerto a entero (int) y verificamos el string de debug
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    # Iniciamos el servidor Flask con la configuración leída
    app.run(debug=debug, host='0.0.0.0', port=port)



