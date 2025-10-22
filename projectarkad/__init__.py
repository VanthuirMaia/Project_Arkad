from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Caminho do banco
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "../instance/arkad.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "projectarkad-secret"

    db.init_app(app)

    # Importa models
    from .models import renda_model
    with app.app_context():
        db.create_all()

    from projectarkad.routes.despesa_routes import despesa_bp

    # Importa rotas
    from .routes.main_routes import main_bp
    from .routes.renda_routes import renda_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(renda_bp)
    app.register_blueprint(despesa_bp)


    return app
