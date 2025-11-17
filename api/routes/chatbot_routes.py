from flask import Blueprint, jsonify, request
from api.utils.chatbot_openai import enviar_mensagem

chatbot_bp = Blueprint("chatbot", __name__)

# Armazena o histórico da conversa globalmente
historico = [{"role": "system", "content": "Você é a Luma, uma assistente educacional amigável e prestativa."}]

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        mensagem = data.get("mensagem", "")

        resposta = "ok"
        if not mensagem:
            return jsonify({"error": "Mensagem vazia"}), 400

        resposta = enviar_mensagem(mensagem, historico)
        return jsonify({"resposta": resposta}), 200
    except Exception as e:
        print("❌ Erro no chatbot:", e)
        return jsonify({"error": "Erro interno no chatbot"}), 500
