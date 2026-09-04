from app import app
from models import db, Product

def seed_data():
    """
    Función para inicializar la base de datos SQLite y cargar datos semilla (seed data).
    Útil para comenzar con datos de prueba sin necesidad de cargarlos a mano.
    """
    # Se requiere el contexto de aplicación de Flask (app_context) 
    # para acceder a la configuración de la base de datos (SQLALCHEMY_DATABASE_URI).
    with app.app_context():
        # db.create_all() lee todos los modelos definidos (como Product)
        # y crea las tablas correspondientes en la base de datos SQL si no existen.
        db.create_all()
        
        # Verificamos si ya existen productos creados previamente para evitar duplicados.
        if Product.query.first():
            print("ℹ️ La base de datos ya contiene productos. No se insertarán duplicados.")
            return

        # Lista de instancias del modelo Product con datos iniciales de prueba
        sample_products = [
            Product(
                title="Fjallraven - Foldsack No. 1 Backpack",
                price=109.95,
                description="Your perfect pack for everyday use and walks in the forest.",
                category="men's clothing",
                image="https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg",
                rating_rate=3.9,
                rating_count=120
            ),
            Product(
                title="Mens Casual Premium Slim Fit T-Shirts",
                price=22.3,
                description="Slim-fit style, contrast raglan long sleeve, three-button henley placket.",
                category="men's clothing",
                image="https://fakestoreapi.com/img/71-3HjGNDUL._AC_SY879._SX._UX._SY._UY_.jpg",
                rating_rate=4.1,
                rating_count=259
            ),
            Product(
                title="Mens Cotton Jacket",
                price=55.99,
                description="Great outerwear jackets for Spring/Autumn/Winter.",
                category="men's clothing",
                image="https://fakestoreapi.com/img/71li-ujtlUL._AC_UX679_.jpg",
                rating_rate=4.7,
                rating_count=500
            )
        ]

        # Agregamos la lista completa a la sesión de SQLAlchemy e impactamos los cambios en SQL (commit)
        db.session.bulk_save_objects(sample_products)
        db.session.commit()
        print("✅ Base de datos SQLite creada e inicializada con productos exitosamente.")

if __name__ == '__main__':
    seed_data()

