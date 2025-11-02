from flask import Blueprint, jsonify, request
from api.utils.relatorio_utils import gerar_relatorio


relatorio_bp = Blueprint('relatorio', __name__)


@relatorio_bp.route("/gerar", methods=["POST"])
def gerar_relatorio_usuario():
    try:
        data = request.get_json(force=True)
        usuario_id = data.get("usuario_id")

        if not usuario_id:
            return jsonify({"error": "ID do usuário é obrigatório."}), 400

        relatorio = gerar_relatorio(usuario_id)
        return jsonify({
            "message": "Relatório gerado com sucesso!",
            "relatorio": relatorio
        }), 200

    except Exception as e:
        print("❌ Erro ao gerar relatório:", e)
        return jsonify({"error": "Erro ao gerar relatório."}), 500

