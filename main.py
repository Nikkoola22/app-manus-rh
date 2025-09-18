import os
import sys
from pathlib import Path

# Configuration portable - détection automatique du répertoire de l'application
APP_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(APP_DIR))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.services.email_service import init_email
from src.routes.auth import auth_bp
from src.routes.agents import agents_bp
from src.routes.services import services_bp
from src.routes.demandes import demandes_bp
from src.routes.arret_maladie import arret_maladie_bp
from src.routes.presence import presence_bp
from src.routes.email import email_bp
from src.routes.planning import planning_bp
from src.routes.test_email import test_email_bp

# Configuration portable des dossiers
STATIC_FOLDER = APP_DIR / 'static'
DATABASE_FOLDER = APP_DIR / 'database'

# Créer les dossiers nécessaires s'ils n'existent pas
STATIC_FOLDER.mkdir(exist_ok=True)
DATABASE_FOLDER.mkdir(exist_ok=True)

app = Flask(__name__, static_folder=str(STATIC_FOLDER))
app.config['SECRET_KEY'] = 'conges-rtt-secret-key-2024'

# Enable CORS for all routes
CORS(app, 
     supports_credentials=True,
     origins=[
         'http://localhost:5173', 
         'http://127.0.0.1:5173',
         'https://app-manus-9r0k68ntb-nikkoola-4074s-projects.vercel.app'  # <-- AJOUTEZ CETTE LIGNE
     ],
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
 )
# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(agents_bp, url_prefix='/api')
app.register_blueprint(services_bp, url_prefix='/api')
app.register_blueprint(demandes_bp, url_prefix='/api')
app.register_blueprint(arret_maladie_bp, url_prefix='/api')
app.register_blueprint(presence_bp, url_prefix='/api')
app.register_blueprint(email_bp, url_prefix='/api')
app.register_blueprint(planning_bp, url_prefix='/api')
app.register_blueprint(test_email_bp, url_prefix='/api')

# Database configuration portable
DATABASE_PATH = DATABASE_FOLDER / 'app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize email service
init_email(app)

# Import all models to ensure they are registered
from src.models.agent import Agent
from src.models.service import Service
from src.models.demande_conge import DemandeConge
from src.models.historique_conge import HistoriqueConge
from src.models.arret_maladie import ArretMaladie
from src.models.presence import Presence

with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = Path(app.static_folder)
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and (static_folder_path / path).exists():
        return send_from_directory(str(static_folder_path), path)
    else:
        index_path = static_folder_path / 'index.html'
        if index_path.exists():
            return send_from_directory(str(static_folder_path), 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
