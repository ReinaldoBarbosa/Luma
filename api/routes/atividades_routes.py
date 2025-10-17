from flask import Blueprint, jsonify, request
from api.utils.atividades_utils import add_atividades, get_all_atividades, delete_atividades, update_atividades, get_atividades_by_id

import hashlib

atividades_bp = Blueprint('atividades', __name__)


@atividades_bp.route('/listar', methods=['GET'])
def listar_atividades():
    try:
        atividades = get_all_atividades()
        return jsonify(atividades), 200
    except Exception as e:
        print(f"Erro ao listar atividades: {e}")
        return jsonify({"error": "Erro ao listar atividades."}), 500


@atividades_bp.route('/criar', methods=['POST'])
def create_atividades_blueprint():
    try:
        data = request.get_json()
        nome = data['nome']
        descriacao = data['descricao']
        link = data['link']
        anexo = data['anexo']
        turma_id = data['turma_is']
        status = data['status']
        data_criacao = data['data_criacao']
        data_entrega = data['data_entrega']


        add_atividades(nome, descriacao, link, anexo, turma_id, status, data_criacao, data_entrega)

    except Exception as e:
        print(f"Erro ao criar atividade: {e}")
        return jsonify({"error": "Erro ao criar ativiidade."}), 500


@atividades_bp.route('/buscar/<int:atividades_id>', methods=['GET'])
def buscar_atividades(atividades_id):
    try:
        atividades = get_atividades_by_id(atividades_id)
        if atividades:
            return jsonify(atividades), 200
        else:
            return jsonify({"error": "Atividade não encontrada."}), 404
    except Exception as e:
        print(f"Erro ao buscar atividade: {e}")
        return jsonify({"error": "Erro ao buscar atividade."}), 500


@atividades_bp.route('/deletar/<int:atividades_id>', methods=['DELETE'])
def excluir_atividades(atividades_id):
    try:
        atividades = get_atividades_by_id(atividades_id)
        if not atividades:
            return jsonify({"error": "Atividade não encontrada."}), 404

        if not atividades:
            return jsonify({"error": "Atividade não encontrada."}), 404

        delete_atividades(atividades_id)
        return jsonify({"message": "Atividade deletada com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao deletar atividade: {e}")
        return jsonify({"error": "Erro ao deletar atividade."}), 500


@atividades_bp.route('/atualizar/<int:atividades_id>', methods=['PUT'])
def atualizar_atividades(atividades_id):
    try:
        data = request.get_json()
        nome = data.get('nome')

        if not nome:
            return jsonify({"error": "Nome da atividade é obrigatório."}), 400

        atividades = get_atividades_by_id(atividades_id)

        if not atividades:
            return jsonify({"error": "Atividade não encontrada."}), 404

        update_atividades(nome, atividades['descricao'], atividades['link'], atividades['anexo'], atividades['turma_id'], atividades['status'], atividades['data_criacao'], atividades['data_entrega'], atividades_id)
        return jsonify({"message": "Atividade atualizada com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao atualizar atividade: {e}")
        return jsonify({"error": "Erro ao atualizar atividade."}), 500


