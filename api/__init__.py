from flask import Flask

def create_app():
    api = Flask(__name__)

    #Importando blueprints
    from .routes.usuario_routes import usuario_bp
    from .routes.turma_routes import turma_bp


    api.register_blueprint(usuario_bp, url_prefix='/usuario')
    api.register_blueprint(turma_bp, url_prefix='/turma')
    

    return api