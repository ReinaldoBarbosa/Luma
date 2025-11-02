from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from api.utils.usuario_utils import add_usuario, get_all_usuario, delete_usuario, update_usuario, get_usuario_by_id, get_usuario_by_email, alterar_senha_usuario

import hashlib

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/listar', methods=['GET'])
def listar_usuarios():
    try:
        usuarios = get_all_usuario()
        return jsonify(usuarios), 200
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return jsonify({"error": "Erro ao listar usuários."}), 500

@usuario_bp.route('/criar', methods=['POST'])
def create_usuario_blueprint():
    try:
        import random
        import string
        import hashlib

        def gerar_ra():
            letra = random.choice(string.ascii_uppercase)
            numeros = ''.join(random.choices(string.digits, k=6))
            return letra + numeros

        def gerar_senha_temporaria(tamanho=10):
            caracteres = string.ascii_letters + string.digits + "!@#$%&*"
            return ''.join(random.choice(caracteres) for _ in range(tamanho))

        def informar_senha(senhat):
            return hashlib.sha256(senhat.encode()).hexdigest()

        def gerar_email_institucional(nome, nivel):
            nome_split = nome.strip().lower().split()
            nome_formatado = f"{nome_split[0]}.{nome_split[-1]}"
            
            dominios = {
                "aluno": "aluno.unip.com",
                "professor": "professor.unip.com",
                "admin": "admin.unip.com"
            }

            dominio = dominios.get(nivel.lower())
            if not dominio:
                raise ValueError("Nível inválido. Use aluno, professor ou admin.")
            
            return f"{nome_formatado}@{dominio}"

        # --- Pega dados enviados ---
        data = request.get_json()
        nome = data.get('nome')
        nivel = data.get('nivel')

        if not nome or not nivel:
            return jsonify({"error": "Campos obrigatórios: nome e nivel"}), 400

        # --- Gera dados automáticos ---
        ra = gerar_ra()
        senha_temporaria = gerar_senha_temporaria()
        senha_hash = informar_senha(senha_temporaria)
        email_institucional = gerar_email_institucional(nome, nivel)
        status = 'ativo'
        primeiro_acesso = True

        # --- Salva no banco ou JSON ---
        add_usuario(nome, ra, email_institucional, senha_hash, nivel, status, primeiro_acesso)

        # --- Retorna os dados e mostra senha temporária ---
        print(f"\nUsuário criado com sucesso:")
        print(f"Email institucional: {email_institucional}")
        print(f"Senha temporária: {senha_temporaria}\n")

        return jsonify({
            "message": "Usuário criado com sucesso.",
            "email_institucional": email_institucional,
            "senha_temporaria": senha_temporaria
        }), 201

    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        return jsonify({"error": "Erro ao criar usuário."}), 500
   

@usuario_bp.route('/buscar/<int:usuario_id>', methods=['GET'])
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

@usuario_bp.route('/deletar/<int:usuario_id>', methods=['DELETE'])  
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

@usuario_bp.route('/atualizar/<int:usuario_id>', methods=['PUT'])
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

@usuario_bp.route('/signin', methods=['POST'])
def sign_in_usuario():
    try:
        import hashlib
        from flask import request, jsonify

        data = request.get_json(force=True)

        if not data or 'email' not in data or 'senha' not in data:
            return jsonify({"error": "Email e senha são obrigatórios."}), 400

        email = data['email']
        senha = data['senha']

        # Criptografa a senha digitada
        senha_digitada_hash = hashlib.sha256(senha.encode()).hexdigest()

        # Busca usuário
        usuarios = get_all_usuario()
        usuario = next(
            (user for user in usuarios if user['email'] == email),
            None
        )

        # Verifica se o usuário existe
        if not usuario:
            return jsonify({"error": "Usuário não encontrado."}), 404

        # Verifica senha
        if usuario['senha'] != senha_digitada_hash:
            return jsonify({"error": "Senha incorreta."}), 401

        # Verifica se é o primeiro acesso
        if usuario.get("primeiro_acesso", False):
            nova_senha = data.get('nova_senha')

            # Se não veio nova senha, pede pra enviar
            if not nova_senha:
                return jsonify({
                    "message": "Primeiro acesso detectado. Por favor, informe uma nova senha.",
                    "necessita_trocar_senha": True
                }), 200

            # Atualiza senha
            nova_senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()
            usuario['senha'] = nova_senha_hash
            usuario['primeiro_acesso'] = False

            # Atualiza no JSON / banco
            atualizar_usuario(usuario)  # <-- função que sobrescreve o usuário salvo

            return jsonify({
                "message": "Senha redefinida com sucesso. Faça login novamente.",
                "usuario": {"email": usuario['email']}
            }), 200

        # Se não é primeiro acesso → login normal
        usuario_sanitizado = usuario.copy()
        usuario_sanitizado.pop("senha", None)

        return jsonify({
            "message": "Login bem-sucedido.",
            "usuario": usuario_sanitizado
        }), 200

    except Exception as e:
        print(f"❌ Erro ao fazer login: {e}")
        return jsonify({"error": "Erro ao fazer login."}), 500


@usuario_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me_usuario():
    try:
        print("📥 Headers recebidos:", request.headers)

        user_id = get_jwt_identity()  # ID que estava no token
        usuario = get_usuario_by_id(user_id)

        if not usuario:
            return jsonify({"error": "Usuário não encontrado."}), 404

        usuario.pop("senha", None)
        return jsonify(usuario), 200

    except Exception as e:
        print(f"❌ Erro ao obter dados do usuário: {e}")
        return jsonify({"error": "Erro ao obter dados do usuário."}), 500

@usuario_bp.route('/alterar_senha', methods=['PUT'])
def alterar_senha():
    try:
        data = request.get_json()
        email = data.get("email")
        nova_senha = data.get("nova_senha")

        def informar_senha(senhat):
            return hashlib.sha256(senhat.encode()).hexdigest()

        senha_cripto = informar_senha(nova_senha)
        
        if not email or not nova_senha:
            return jsonify({"error": "Email e nova senha são obrigatórios."}), 400

        usuario = get_usuario_by_email(email)
        if not usuario:
            return jsonify({"error": "Usuário não encontrado."}), 404

        alterar_senha_usuario(email, senha_cripto)
        return jsonify({"message": "Senha atualizada com sucesso!"}), 200

    except Exception as e:
        print(f"Erro ao alterar senha: {e}")
        return jsonify({"error": "Erro ao alterar senha."}), 500
