from flask import Flask

def create_app():
    api = Flask(__name__)

    #Importando blueprints
    from .routes.professor_routes import professor_bp


    api.register_blueprint(professor_bp, url_prefix='/professores')
    

    return api