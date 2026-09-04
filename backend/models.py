from flask_sqlalchemy import SQLAlchemy

# Inicializamos la instancia de SQLAlchemy.
# Este objeto 'db' nos permitirá interactuar con la base de datos SQL usando clases de Python (ORM).
db = SQLAlchemy()

# Definimos el modelo de la tabla 'Product'.
# Heredar de db.Model le indica a SQLAlchemy que esta clase representa una tabla en la DB SQL.
class Product(db.Model):
    # Nombre exacto de la tabla en la base de datos SQL
    __tablename__ = 'products'

    # Columnas de la tabla:
    # 1. Clave primaria única e autoincremental
    id = db.Column(db.Integer, primary_key=True)
    # 2. Título del producto (cadena de texto de máx 200 caracteres, no puede ser nulo)
    title = db.Column(db.String(200), nullable=False)
    # 3. Precio del producto (número flotante/decimal, no nulo)
    price = db.Column(db.Float, nullable=False)
    # 4. Descripción detallada (texto largo sin límite fijo)
    description = db.Column(db.Text, nullable=True)
    # 5. Categoría del producto (ej: "men's clothing", "electronics")
    category = db.Column(db.String(100), nullable=False)
    # 6. URL de la imagen del producto
    image = db.Column(db.String(500), nullable=True)
    # 7. Calificación promedio (estrellas/rating)
    rating_rate = db.Column(db.Float, default=0.0)
    # 8. Cantidad de opiniones/reseñas recibidas
    rating_count = db.Column(db.Integer, default=0)

    # Método de conveniencia para convertir el objeto de Python (registro SQL) 
    # a un Diccionario, facilitando su respuesta en formato JSON a la API.
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'description': self.description,
            'category': self.category,
            'image': self.image,
            'rating': {
                'rate': self.rating_rate,
                'count': self.rating_count
            }
        }

