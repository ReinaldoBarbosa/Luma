from flask import Blueprint, jsonify, request
from api.utils.usuario_utils import add_usuario, get_all_usuario, delete_usuario, update_usuario, get_usuario_by_id

import hashlib

atividades_bp = Blueprint('usuario', __name__)


@atividades_bp.route('/listar', methods=['GET'])
def listar_usuarios():
    try:
        usuarios = get_all_usuario()
        return jsonify(usuarios), 200
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return jsonify({"error": "Erro ao listar usuários."}), 500


@atividades_bp.route('/criar', methods=['POST'])
def create_usuario_blueprint():
    try:
        def gerar_ra():
            import random
            import string
            letra = random.choice(string.ascii_uppercase)
            numeros = ''.join(random.choices(string.digits, k=6))
            return letra + numeros

        def informar_senha(senha):
            return hashlib.sha256(senha.encode()).hexdigest()

        data = request.get_json()
        nome = data['nome']
        email = data['email']
        senha = data['senha']
        nivel = data['nivel']
        status = 'ativo'
        ra = gerar_ra()

        if email.split('@')[1] == "professor.unip.com" or email.split('@')[1] == "aluno.unip.com" or email.split('@')[
            1] == "admin.unip.com":
            add_usuario(nome, ra, email, informar_senha(senha), nivel, status)
            return jsonify({"message": "Usuario criado com sucesso."}), 201


    except Exception as e:
        print(f"Erro ao criar professor: {e}")
        return jsonify({"error": "Erro ao criar professor."}), 500


@atividades_bp.route('/buscar/<int:usuario_id>', methods=['GET'])
def buscar_usuario(usuario_id):
    try:
        usuario = get_usuario_by_id(usuario_id)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({"error": "Usuario não encontrado."}), 404
    except Exception as e:
        print(f"Erro ao buscar usuario: {e}")
        return jsonify({"error": "Erro ao buscar usuario."}), 500


@atividades_bp.route('/deletar/<int:usuario_id>', methods=['DELETE'])
def excluir_usuario(usuario_id):
    try:
        usuario = get_usuario_by_id(usuario_id)
        if not usuario:
            return jsonify({"error": "Usuario não encontrado."}), 404

        if not usuario:
            return jsonify({"error": "Usuario não encontrado."}), 404

        delete_usuario(usuario_id)
        return jsonify({"message": "Usuario deletado com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao deletar usuario: {e}")
        return jsonify({"error": "Erro ao deletar usuario."}), 500


@atividades_bp.route('/atualizar/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    try:
        data = request.get_json()
        nome = data.get('nome')

        if not nome:
            return jsonify({"error": "Nome é obrigatório."}), 400

        usuario = get_usuario_by_id(usuario_id)

        if not usuario:
            return jsonify({"error": "Usuario não encontrado."}), 404

        update_usuario(nome, usuario['ra'], usuario['email'], usuario['senha'], usuario['nivel'], usuario_id)
        return jsonify({"message": "Usuario atualizado com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao atualizar usuario: {e}")
        return jsonify({"error": "Erro ao atualizar usuario."}), 500


@atividades_bp.route('/signin', methods=['POST'])
def sign_in_usuario():
    try:
        data = request.get_json()
        email = data['email']
        senha = data['senha']

        senha_digitada_hash = hashlib.sha256(senha.encode()).hexdigest()
        usuarios = get_all_usuario()
        usuario = next((user for user in usuarios if user['email'] == email and user['senha'] == senha_digitada_hash),
                       None)

        if usuario:
            return jsonify({"message": "Login bem-sucedido."}), 200
        else:
            return jsonify({"error": "Credenciais inválidas."}), 401
    except Exception as e:
        print(f"Erro ao fazer login: {e}")
        return jsonify({"error": "Erro ao fazer login."}), 500