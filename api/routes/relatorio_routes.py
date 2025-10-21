from flask import Blueprint, jsonify, request
from api.utils.relatório_utils import add_relatório, get_all_relatório, delete_relatório, update_relatório, get_relatório_by_id

import hashlib

relatório_bp = Blueprint('relatório', __name__)


@relatório_bp.route('/listar', methods=['GET'])
def listar_relatório():
    try:
        relatório = get_all_relatório()
        return jsonify(relatório), 200
    except Exception as e:
        print(f"Erro ao listar relatórios: {e}")
        return jsonify({"error": "Erro ao listar relatórios."}), 500


@relatório_bp.route('/criar', methods=['POST'])
def create_relatório_blueprint():
    try:
        data = request.get_json()
        usuario_id = data['usuario_id']
        media_geral = data['media_geral']
        total_atividade = data['total_atividades']
        data_geracao = data['data_geracao']

        add_relatório(usuario_id, media_geral, total_atividade, data_geracao)

    except Exception as e:
        print(f"Erro ao criar relatório.: {e}")
        return jsonify({"error": "Erro ao criar relatório.."}), 500


@relatório_bp.route('/buscar/<int:relatório_id>', methods=['GET'])
def buscar_relatório(relatório_id):
    try:
        relatório = get_relatório_by_id(relatório_id)
        if relatório:
            return jsonify(relatório), 200
        else:
            return jsonify({"error": "Relatório não encontrado."}), 404
    except Exception as e:
        print(f"Erro ao buscar relatório.: {e}")
        return jsonify({"error": "Erro ao buscar relatório."}), 500


@relatório_bp.route('/deletar/<int:relatório_id>', methods=['DELETE'])
def excluir_relatório(relatório_id):
    try:
        relatório = get_relatório_by_id(relatório_id)
        if not relatório:
            return jsonify({"error": "Relatório não encontrado."}), 404

        if not relatório:
            return jsonify({"error": "Relatório não encontrado."}), 404

        delete_relatório(relatório_id)
        return jsonify({"message": "Relatório deletado com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao deletar urelatório: {e}")
        return jsonify({"error": "Erro ao deletar relatório."}), 500


@relatório_bp.route('/atualizar/<int:relatório_id>', methods=['PUT'])
def atualizar_relatório(relatório_id):
    try:
        data = request.get_json()
        nome = data.get('nome')

        if not nome:
            return jsonify({"error": "Nome é obrigatório."}), 400

        relatório = get_relatório_by_id(relatório_id)

        if not relatório:
            return jsonify({"error": "Relatório não encontrado."}), 404

        update_relatório(nome, relatório['usuario-id'], relatório['media_geral'], relatório['total_atividades'], relatório['data_geracao'], relatório_id)
        return jsonify({"message": "Relatório atualizado com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao atualizar relatório: {e}")
        return jsonify({"error": "Erro ao atualizar relatório."}), 500


