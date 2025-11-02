from flask import Blueprint, jsonify, request
from api.utils.atividades_utils import (
    add_atividade, 
    get_all_atividade, 
    delete_atividade, 
    update_atividade, 
    get_atividades_by_usuario, 
    get_atividade_by_id, 
    salvar_resposta_atividade,
    get_respostas_by_atividade
)

import os
import datetime
from werkzeug.utils import secure_filename

atividade_bp = Blueprint('atividade', __name__)


@atividade_bp.route('/listar', methods=['GET'])
def listar_atividade():
    try:
        atividade = get_all_atividade()
        return jsonify(atividade), 200
    except Exception as e:
        print(f"Erro ao listar atividade: {e}")
        return jsonify({"error": "Erro ao listar atividade."}), 500



@atividade_bp.route('/criar', methods=['POST'])
def create_atividade_blueprint():
    try:
        # Detecta automaticamente o tipo de conteúdo
        if request.content_type.startswith('application/json'):
            data = request.get_json()
            nome = data.get('nome')
            descricao = data.get('descricao')
            link = data.get('link')
            turma_id = data.get('turma_id')
            data_entrega = data.get('data_entrega')
            status = data.get('status', 'em_andamento')
            anexo = data.get('anexo')  # apenas o caminho
            caminho_anexo = anexo
            usuario_id = data.get('usuario_id')  # mantém o mesmo valor
        else:
            nome = request.form.get('nome')
            descricao = request.form.get('descricao')
            link = request.form.get('link')
            turma_id = request.form.get('turma_id')
            data_entrega = request.form.get('data_entrega')
            status = request.form.get('status', 'em_andamento')
            arquivo = request.files.get('anexo')
            usuario_id = request.form.get('usuario_id')  # mantém o mesmo valor

            caminho_anexo = None
            

        print("Criando atividade:", nome, turma_id, data_entrega, status, anexo, link, descricao)
        # Verificação dos campos obrigatórios
        if not nome or not turma_id or not usuario_id:
            return jsonify({"error": "Nome, ID da turma e ID do usuário são obrigatórios."}), 400

        # Se houver arquivo, salva
        caminho_anexo = None
    

        # Define data de criação
        data_criacao = datetime.date.today()

        # Chama a função de inserção no banco
        add_atividade(nome, descricao, link, caminho_anexo, turma_id, usuario_id, status, data_criacao, data_entrega)

        return jsonify({"message": "Atividade criada com sucesso."}), 201

    except Exception as e:
        print(f"Erro ao criar atividade: {e}")
        return jsonify({"error": "Erro ao criar atividade."}), 500


@atividade_bp.route('/buscar/<int:atividade_id>', methods=['GET'])
def buscar_atividade(atividade_id):
    try:
        atividade = get_atividade_by_id(atividade_id)
        if atividade:
            return jsonify(atividade), 200
        else:
            return jsonify({"error": "Atividade não encontrada."}), 404
    except Exception as e:
        print(f"Erro ao buscar atividade: {e}")
        return jsonify({"error": "Erro ao buscar atividade."}), 500


@atividade_bp.route('/deletar/<int:atividade_id>', methods=['DELETE'])
def excluir_atividade(atividade_id):
    try:
        atividade = get_atividade_by_id(atividade_id)
        if not atividade:
            return jsonify({"error": "Atividade não encontrada."}), 404

        if not atividade:
            return jsonify({"error": "Atividade não encontrada."}), 404

        delete_atividade(atividade_id)
        return jsonify({"message": "Atividade deletada com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao deletar atividade: {e}")
        return jsonify({"error": "Erro ao deletar atividade."}), 500


@atividade_bp.route('/atualizar/<int:atividade_id>', methods=['PUT'])
def atualizar_atividade(atividade_id):
    try:
        data = request.get_json()
        nome = data.get('nome')

        if not nome:
            return jsonify({"error": "Nome da atividade é obrigatório."}), 400

        atividade = get_atividade_by_id(atividade_id)

        if not atividade:
            return jsonify({"error": "Atividade não encontrada."}), 404

        update_atividade(nome, atividade['descricao'], atividade['link'], atividade['anexo'], atividade['turma_id'], atividade['status'], atividade['data_criacao'], atividade['data_entrega'], atividade_id)
        return jsonify({"message": "Atividade atualizada com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao atualizar atividade: {e}")
        return jsonify({"error": "Erro ao atualizar atividade."}), 500


@atividade_bp.route('/minhas/<int:usuario_id>', methods=['GET'])
def minhas_atividades(usuario_id):
    try:
        atividades = get_atividades_by_usuario(usuario_id)
        return jsonify(atividades), 200
    except Exception as e:
        print(f"Erro ao listar atividades do usuário: {e}")
        return jsonify({"error": "Erro ao listar atividades do usuário."}), 500


@atividade_bp.route('/responder', methods=['POST'])
def responder_atividade():
    try:
        data = request.get_json()
        atividade_id = data.get('atividade_id')
        aluno_id = data.get('aluno_id')
        resposta = data.get('resposta')

        if not atividade_id or not aluno_id or not resposta:
            return jsonify({"error": "ID da atividade, ID do aluno e resposta são obrigatórios."}), 400

        atividade = get_atividade_by_id(atividade_id)
        if not atividade:
            return jsonify({"error": "Atividade não encontrada."}), 404

        # Salva a resposta e atualiza o status da atividade
        salvar_resposta_atividade(atividade_id, aluno_id, resposta)

        return jsonify({"message": "Resposta enviada com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao responder atividade: {e}")
        return jsonify({"error": "Erro ao responder atividade."}), 500


@atividade_bp.route('/respostas/<int:atividade_id>', methods=['GET'])
def listar_respostas_atividade(atividade_id):
    try:
        respostas = get_respostas_by_atividade(atividade_id)  # função no seu util
        return jsonify({"respostas": respostas}), 200
    except Exception as e:
        print(f"Erro ao listar respostas da atividade: {e}")
        return jsonify({"error": "Erro ao listar respostas da atividade."}), 500

