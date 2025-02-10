from flask import Flask
from flask_cors import CORS

from app.api_endpoints import api_bp
from app.extensions import bcrypt, login_manager, swagger
from app.models import db, Destination, SubscriptionPlan, User
from app.mvc_endpoints import mvc_bp


def create_app(config_class='config.Config'):
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(config_class)
    CORS(app)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'mvc.login'
    swagger.init_app(app)

    app.register_blueprint(mvc_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()
        seed_data()

    return app


def seed_data():
    if not Destination.query.first():
        destinations = [
            'La Corunya', 'Lugo', 'Pontevedra', 'Ourense', 'Leon', 'Asturias', 'Zamora', 'Salamanca', 'Caceres',
            'Badajoz', 'Huelva', 'Sevilla', 'Cadiz', 'Malaga', 'Cordoba', 'Ciudad Real', 'Toledo', 'Avila',
            'Valladolid', 'Segovia', 'Burgos', 'Palencia', 'Cantabria', 'Vizcaya', 'Guipuzcoa', 'Alava',
            'La Rioja', 'Soria', 'Guadalajara', 'Madrid', 'Cuenca', 'Granada', 'Jaen', 'Almeria', 'Murcia',
            'Albacete', 'Alicante', 'Valencia', 'Teruel', 'Castellon', 'Zaragoza', 'Navarra', 'Lleida',
            'Huesca', 'Girona', 'Barcelona', 'Tarragona', 'Menorca', 'Mallorca', 'Ibiza', 'Cabrera',
            'Formentera', 'Ceuta', 'La Palma', 'Melilla', 'Hierro', 'Gomera', 'Tenerife', 'Grancanaria',
            'Fuerteventura', 'Lanzarote'
        ]
        for name in destinations:
            destination = Destination(name=name)
            db.session.add(destination)

    if not SubscriptionPlan.query.first():
        plans_data = [
            {"name": "Standard", "price": 10, "insurance_type": "1 month", "tracking": "Basic"},
            {"name": "Premium", "price": 15, "insurance_type": "6 months", "tracking": "24/7"},
            {"name": "Ultra", "price": 20, "insurance_type": "12 months", "tracking": "24/7"},
        ]
        for plan in plans_data:
            subscription_plan = SubscriptionPlan(**plan)
            db.session.add(subscription_plan)

    db.session.commit()
