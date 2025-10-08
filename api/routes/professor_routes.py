from flask import Blueprint, jsonify, request
from api.utils.professores_utils import add_professor, get_all_professores

professor_bp = Blueprint('professor', __name__)

@professor_bp.route('/listar', methods=['GET'])
def listar_professores():
    try:
        professores = get_all_professores()
        return jsonify(professores), 200
    except Exception as e:
        print(f"Erro ao listar professores: {e}")
        return jsonify({"error": "Erro ao listar professores."}), 500

@professor_bp.route('/criar', methods=['POST'])
def create_professor_blueprint():
    try:
        data = request.get_json()
        nome = data['nome']
        disciplina = data['disciplina']

        if not nome or not disciplina:
            return jsonify({"error": "Nome e disciplina são obrigatórios."}), 400
        
        add_professor(nome, disciplina)
        return jsonify({"message": "Professor criado com sucesso."}), 201
    except Exception as e:
        print(f"Erro ao criar professor: {e}")
        return jsonify({"error": "Erro ao criar professor."}), 500    

@professor_bp.route('/buscar/<int:professor_id>', methods=['GET'])
def buscar_professor(professor_id):
    try:
        professores = get_all_professores()
        professor = next((prof for prof in professores if prof['id'] == professor_id), None)
        if professor:
            return jsonify(professor), 200
        else:
            return jsonify({"error": "Professor não encontrado."}), 404
    except Exception as e:
        print(f"Erro ao buscar professor: {e}")
        return jsonify({"error": "Erro ao buscar professor."}), 500    
    

                