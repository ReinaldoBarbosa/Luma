from flask import Flask
from flask_jwt_extended import JWTManager
import os

jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # ⚙️ Configuração JWT
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "chave_dev_segura")
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"

    # 🧩 Importando blueprints
    from .routes.usuario_routes import usuario_bp
    from .routes.turma_routes import turma_bp
    from .routes.material_routes import material_bp
    from .routes.notas_routes import notas_bp
    from .routes.relatorio_routes import relatorio_bp
    from .routes.atividades_routes import atividade_bp
    from .routes.chatbot_routes import chatbot_bp

    # 🧱 Registrando rotas
    app.register_blueprint(usuario_bp, url_prefix="/usuario")
    app.register_blueprint(turma_bp, url_prefix="/turma")
    app.register_blueprint(material_bp, url_prefix="/material")
    app.register_blueprint(notas_bp, url_prefix="/notas")
    app.register_blueprint(relatorio_bp, url_prefix="/relatorio")
    app.register_blueprint(atividade_bp, url_prefix="/atividade")
    app.register_blueprint(chatbot_bp, url_prefix="/chatbot")

    # 🔐 Inicializa JWT
    jwt.init_app(app)

    # ✅ Log de confirmação
    print("✅ JWT configurado e Blueprints carregados.")

    return app
