from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.secret_key = os.getenv('SECRET_KEY', 'sua_chave_secreta_aqui')
    
    from app.controllers.transacao_controller import transacao_bp
    from app.controllers.categoria_controller import categoria_bp
    
    app.register_blueprint(transacao_bp)
    app.register_blueprint(categoria_bp)
    
    return app