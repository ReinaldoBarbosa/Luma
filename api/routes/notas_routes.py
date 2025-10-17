from flask import Blueprint, jsonify, request
from api.utils.notas_utils import add_notas, get_all_notas, delete_notas, update_notas, get_notas_by_id

import hashlib

notas_bp = Blueprint('notas', __name__)


@notas_bp.route('/listar', methods=['GET'])
def listar_notas():
    try:
        notas = get_all_notas()
        return jsonify(notas), 200
    except Exception as e:
        print(f"Erro ao listar notas: {e}")
        return jsonify({"error": "Erro ao listar notas."}), 500


@notas_bp.route('/criar', methods=['POST'])
def create_notas_blueprint():
    try:
        data = request.get_json()
        usuario_id = data['usuario-id']
        atividade_id = data['atividade_id']
        nota = data['nota']
        status = 'ativo'

        add_notas(usuario_id, atividade_id, nota)


    except Exception as e:
        print(f"Erro ao cadastrar nota: {e}")
        return jsonify({"error": "Erro ao cadastrar nota."}), 500


@notas_bp.route('/buscar/<int:notas_id>', methods=['GET'])
def buscar_notas(notas_id):
    try:
        notas = get_notas_by_id(notas_id)
        if notas:
            return jsonify(notas), 200
        else:
            return jsonify({"error": "Nota não encontrada."}), 404
    except Exception as e:
        print(f"Erro ao buscar nota: {e}")
        return jsonify({"error": "Erro ao buscar nota."}), 500


@notas_bp.route('/deletar/<int:notas_id>', methods=['DELETE'])
def excluir_notas(notas_id):
    try:
        notas = get_notas_by_id(notas_id)
        if not notas:
            return jsonify({"error": "Nota não encontrada."}), 404

        if not notas:
            return jsonify({"error": "Nota não encontrada."}), 404

        delete_notas(notas_id)
        return jsonify({"message": "Nota deletada com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao deletar nota: {e}")
        return jsonify({"error": "Erro ao deletar nota."}), 500


@notas_bp.route('/atualizar/<int:notas_id>', methods=['PUT'])
def atualizar_notas(notas_id):
    try:
        data = request.get_json()
        nome = data.get('nome')

        if not nome:
            return jsonify({"error": "Nome é obrigatório."}), 400

        notas = get_notas_by_id(notas_id)

        if not notas:
            return jsonify({"error": "Nota não encontrada."}), 404

        update_notas(nome, notas['usuario_id'], notas['atividade_id'], notas['nota'], notas_id)
        return jsonify({"message": "Usuario atualizado com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao atualizar nota.: {e}")
        return jsonify({"error": "Erro ao atualizar nota."}), 500


