from flask import Blueprint, jsonify, request
from api.utils.turmas_utils import add_turma, get_all_turmas, delete_turma, update_turma, get_turma_by_id, get_turmas_by_professor

turma_bp = Blueprint('turma', __name__)

@turma_bp.route('/listar', methods=['GET'])
def listar_turmas():
    try:
        turmas = get_all_turmas()
        return jsonify(turmas), 200
    except Exception as e:
        print(f"Erro ao listar turmas: {e}")
        return jsonify({"error": "Erro ao listar turmas."}), 500
    
@turma_bp.route('/criar', methods=['POST'])  
def criar_turma():
    try:
        data = request.get_json()
        print(data)

        if not data:
            return jsonify({"error": "Requisito inválido, corpo vazio."}), 400
        
        nome = data.get('nome')
        professor_id = data.get('professor_id')

        if not nome or not professor_id:
            return jsonify({"error": "Nome e ID do professor são obrigatórios."}), 400

        add_turma(nome, professor_id, "ativo")
        return jsonify({"message": "Turma criada com sucesso."}), 201
    except Exception as e:
        print(f"Erro ao criar turma: {e}")
        return jsonify({"error": "Erro ao criar turma."}), 500

@turma_bp.route('/deletar/<int:turma_id>', methods=['DELETE'])
def excluir_turma(turma_id):
    try:
        turma = get_turma_by_id(turma_id)
        if not turma:
            return jsonify({"error": "Turma não encontrada."}), 404

        delete_turma(turma_id)
        return jsonify({"message": "Turma deletada com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao deletar turma: {e}")
        return jsonify({"error": "Erro ao deletar turma."}), 500
    
@turma_bp.route('/atualizar/<int:turma_id>', methods=['PUT'])
def atualizar_turma(turma_id):
    try:
        data = request.get_json()
        nome = data.get('nome')
        professor_id = data.get('professor_id')
        status = data.get('status')

        turma = get_turma_by_id(turma_id)
        if not turma:
            return jsonify({"error": "Turma não encontrada."}), 404

        update_turma(turma_id, nome, professor_id, status)
        return jsonify({"message": "Turma atualizada com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao atualizar turma: {e}")
        return jsonify({"error": "Erro ao atualizar turma."}), 500

@turma_bp.route('/buscar/<int:turma_id>', methods=['GET'])
def buscar_turma(turma_id):
    try:
        turma = get_turma_by_id(turma_id)
        if turma:
            return jsonify(dict(turma)), 200
        else:
            return jsonify({"error": "Turma não encontrada."}), 404
    except Exception as e:
        print(f"Erro ao buscar turma: {e}")
        return jsonify({"error": "Erro ao buscar turma."}), 500

@turma_bp.route('/professor/<int:turma_id>', methods=['GET'])
def listar_turmas_professor(turma_id):
    try:
        turmas = get_turmas_by_professor(turma_id)
        return jsonify([dict(turma) for turma in turmas]), 200
    except Exception as e:
        print(f"Erro ao listar turmas do professor: {e}")
        return jsonify({"error": "Erro ao listar turmas do professor."}), 500         

@turma_bp.route('/add/aluno/<int:turma_id>', methods=['POST'])
def adicionar_aluno_turma(turma_id):
    try:
        data = request.get_json()
        aluno_id = data.get('aluno_id')

        if not aluno_id:
            return jsonify({"error": "ID do aluno é obrigatório."}), 400

        # Lógica para adicionar o aluno à turma

        
        # Exemplo: add_aluno_to_turma(turma_id, aluno_id)

        return jsonify({"message": "Aluno adicionado à turma com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao adicionar aluno à turma: {e}")
        return jsonify({"error": "Erro ao adicionar aluno à turma."}), 500
         