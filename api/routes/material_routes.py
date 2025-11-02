from flask import Blueprint, request, jsonify
from api.utils.material_utils import (
    add_material, 
    get_all_material, 
    delete_material, 
    update_material,
    get_material_by_id, 
    get_materiais_by_turma
)

material_bp = Blueprint('material', __name__)


@material_bp.route('/listar', methods=['GET'])
def listar_material():
    try:
        materiais = get_all_material()
        return jsonify(materiais), 200
    except Exception as e:
        print(f"Erro ao listar materiais: {e}")
        return jsonify({"error": "Erro ao listar materiais."}), 500

@material_bp.route('/criar', methods=['POST'])
def criar_material():
    try:
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        link = request.form.get('link')
        turma_id = request.form.get('turma_id')

        if not nome or not turma_id:
            return jsonify({"error": "Nome e ID da turma são obrigatórios."}), 400

        caminho_anexo = None

        add_material(nome, descricao, link, caminho_anexo, turma_id, "ativo")
        return jsonify({"message": "Material criado com sucesso."}), 201
    except Exception as e:
        print(f"Erro ao criar material: {e}")
        return jsonify({"error": "Erro ao criar material."}), 500    

@material_bp.route('/deletar/<int:material_id>', methods=['DELETE'])
def excluir_material(material_id):
    try:
        material = get_material_by_id(material_id)
        if not material:
            return jsonify({"error": "Material não encontrado."}), 404

        delete_material(material_id)
        return jsonify({"message": "Material deletado com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao deletar material: {e}")
        return jsonify({"error": "Erro ao deletar material."}), 500

@material_bp.route('/atualizar/<int:material_id>', methods=['PUT'])
def atualizar_material(material_id):
    try:
        data = request.form
        nome = data.get('nome')
        descricao = data.get('descricao')
        link = data.get('link')
        status = data.get('status')
        anexo = None
        material = get_material_by_id(material_id)
        if not material:
            return jsonify({"error": "Material não encontrado."}), 404
       
        update_material(nome, descricao, link, anexo, status, material_id)
        return jsonify({"message": "Material atualizado com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao atualizar material: {e}")
        return jsonify({"error": "Erro ao atualizar material."}), 500
    
@material_bp.route('/listar/<int:turma_id>', methods=['GET'])
def listar_material_turma(turma_id):
    try:
        materiais = get_materiais_by_turma(turma_id)
        return jsonify(materiais), 200
    except Exception as e:
        print(f"Erro ao listar materiais da turma: {e}")
        return jsonify({"error": "Erro ao listar materiais da turma."}), 500

@material_bp.route('/turma/<int:material_id>', methods=['GET'])
def ver_material_turma(material_id):
    try:
        material = get_material_by_id(material_id)
        if not material:
            return jsonify({"message": "Nenhum material encontrado para esta turma."}), 404
        return jsonify({"materiais": [material]}), 200
    except Exception as e:
        print(f"Erro ao buscar materiais da turma: {e}")
        return jsonify({"error": "Erro ao buscar materiais da turma."}), 500        