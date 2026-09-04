import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import db, Product

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Habilitamos CORS (Cross-Origin Resource Sharing)
# Esto es esencial para permitir que el frontend (HTML/JS) consuma nuestra API
# sin ser bloqueado por las políticas de seguridad del navegador.
CORS(app)

# Configuración del path absoluto para almacenar el archivo de base de datos SQLite 'ecommerce.db'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'ecommerce.db')
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
    # Iniciamos el servidor de desarrollo de Flask en el puerto 5000 con modo debug activo
    app.run(debug=True, port=5000)



