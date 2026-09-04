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

if __name__ == '__main__':
    # Iniciamos el servidor de desarrollo de Flask en el puerto 5000 con modo debug activo
    app.run(debug=True, port=5000)


