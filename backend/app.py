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

if __name__ == '__main__':
    # Leemos el puerto y el modo debug desde las variables de entorno (.env)
    # Convertimos el puerto a entero (int) y verificamos el string de debug
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    # Iniciamos el servidor Flask con la configuración leída
    app.run(debug=debug, host='0.0.0.0', port=port)



