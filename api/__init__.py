from flask import Flask

def create_app():
    api = Flask(__name__)

    #Importando blueprints
    from .routes.usuario_routes import usuario_bp
    from .routes.turma_routes import turma_bp
    from .routes.material_routes import material_bp
    from .routes.notas_routes import notas_bp
    from .routes.relatorio_routes import relatorio_bp
    from .routes.atividades_routes import atividades_bp


    api.register_blueprint(usuario_bp, url_prefix='/usuario')
    api.register_blueprint(turma_bp, url_prefix='/turma')
    api.register_blueprint(material_bp, url_prefix='/material')
    api.register_blueprint(notas_bp, url_prefix='/notas')
    api.register_blueprint(relatorio_bp, url_prefix='/relatorio')
    api.register_blueprint(atividades_bp, url_prefix='/atividades')


    return api