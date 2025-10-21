import sqlite3

DB_PATH = "api/app.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_atividades():
    conn = get_db_connection()
    cursor = conn.cursor()
    atividades = cursor.execute("SELECT * FROM atividades").fetchall()
    conn.close()
    return [dict(atividades) for turma in atividades]


def add_atividades(nome, descricao, link, anexo, turma_id, status, data_criacao, data_entrega):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO turma (nome, descricao, link, anexo, turma_id, status, data_criacao, data_entrega) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(nome, descricao, link, anexo, turma_id, status, data_criacao, data_entrega))
    conn.commit()
    conn.close()


def delete_atividades(atividades_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM atividades WHERE id = ?", (atividades_id,))
    conn.commit()
    conn.close()


def update_atividades(atividades_id, nome, descricao, link, anexo, turma_id, status, data_criacao, data_entrega):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE turma SET nome = ?, descricao = ?, link = ?, anexo = ?, turma_id = ? , status = ?, data_criacao = ?, data_entrega = ? WHERE id = ?",
                   (nome, descricao, link, anexo, turma_id, status, data_criacao, data_entrega))
    conn.commit()
    conn.close()


def get_atividades_by_id(atividades_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM atividades WHERE id = ?", (atividades_id,))
    atividades = cursor.fetchone()
    conn.close()
    return atividades


def get_atividades_by_professor(atividades_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM atividades WHERE professor_id = ?", (atividades_id,))
    atividades = cursor.fetchall()
    conn.close()
    return atividades
