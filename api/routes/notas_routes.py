from flask import Blueprint, jsonify, request
from api.utils.notas_utils import (
    get_db_connection,
    get_all_notas,
    delete_nota,
    update_nota,
    get_notas_by_usuario,
    get_notas_by_turma
)

import sqlite3

# Corrigido: blueprint deve ser notas_bp (não atividade_bp)
notas_bp = Blueprint('notas_bp', __name__)


# 🔹 Lançar ou atualizar nota (somente professor)
@notas_bp.route('/lancar', methods=['POST'])
def lancar_nota():
    try:
        data = request.get_json()
        professor_id = data.get('professor_id')
        aluno_id = data.get('aluno_id')
        atividade_id = data.get('atividade_id')
        nota = data.get('nota')

        # Validação de campos obrigatórios
        if not all([aluno_id, atividade_id]) or nota is None:
            return jsonify({"error": "Todos os campos são obrigatórios."}), 400

        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Verificar se o usuário é realmente professor
        cursor.execute("SELECT nivel FROM usuario WHERE id = ?", (professor_id,))
        user = cursor.fetchone()
        if not user or user["nivel"] != "professor":
            conn.close()
            return jsonify({"error": "Apenas professores podem lançar notas."}), 403

        # Verificar se a nota já foi lançada
        cursor.execute("""
            SELECT id FROM nota
            WHERE usuario_id = ? AND atividade_id = ?
        """, (aluno_id, atividade_id))
        nota_existente = cursor.fetchone()

        if nota_existente:
            # Atualiza a nota existente
            cursor.execute("""
                UPDATE nota
                SET nota = ?
                WHERE usuario_id = ? AND atividade_id = ?
            """, (nota, aluno_id, atividade_id))
        else:
            # Lança uma nova nota
            cursor.execute("""
                INSERT INTO nota (usuario_id, atividade_id, nota)
                VALUES (?, ?, ?)
            """, (aluno_id, atividade_id, nota))

        conn.commit()
        conn.close()

        return jsonify({"message": "Nota lançada ou atualizada com sucesso."}), 200

    except Exception as e:
        print(f"Erro ao lançar nota: {e}")
        return jsonify({"error": "Erro ao lançar nota."}), 500


# 🔹 Listar todas as notas de um aluno
@notas_bp.route('/aluno/<int:aluno_id>', methods=['GET'])
def listar_notas_aluno(aluno_id):
    try:
        notas = get_notas_by_usuario(aluno_id)
        return jsonify(notas), 200
    except Exception as e:
        print(f"Erro ao listar notas: {e}")
        return jsonify({"error": "Erro ao listar notas."}), 500


# 🔹 Listar todas as notas (somente para debug/admin)
@notas_bp.route('/nota/todas', methods=['GET'])
def listar_todas_notas():
    try:
        notas = get_all_notas()
        return jsonify(notas), 200
    except Exception as e:
        print(f"Erro ao listar todas as notas: {e}")
        return jsonify({"error": "Erro ao listar todas as notas."}), 500


# 🔹 Deletar uma nota
@notas_bp.route('/nota/<int:nota_id>', methods=['DELETE'])
def deletar_nota(nota_id):
    try:
        delete_nota(nota_id)
        return jsonify({"message": "Nota deletada com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao deletar nota: {e}")
        return jsonify({"error": "Erro ao deletar nota."}), 500


# 🔹 Atualizar uma nota específica
@notas_bp.route('/nota/<int:nota_id>', methods=['PUT'])
def atualizar_nota(nota_id):
    try:
        data = request.get_json()
        usuario_id = data.get('usuario_id')
        atividade_id = data.get('atividade_id')
        nota = data.get('nota')

        if not all([usuario_id, atividade_id]) or nota is None:
            return jsonify({"error": "Todos os campos são obrigatórios."}), 400

        update_nota(nota_id, usuario_id, atividade_id, nota)
        return jsonify({"message": "Nota atualizada com sucesso."}), 200

    except Exception as e:
        print(f"Erro ao atualizar nota: {e}")
        return jsonify({"error": "Erro ao atualizar nota."}), 500

# 🔹 Ver todas as notas de todos os alunos de uma turma
@notas_bp.route('/nota/turma/<int:turma_id>', methods=['GET'])
def ver_notas_turma(turma_id):
    try:
        notas = get_notas_by_turma(turma_id)
        if not notas:
            return jsonify({"message": "Nenhuma nota encontrada para esta turma."}), 404
        return jsonify(notas), 200
    except Exception as e:
        print(f"Erro ao buscar notas da turma: {e}")
        return jsonify({"error": "Erro ao buscar notas da turma."}), 500