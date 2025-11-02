import sqlite3

DB_PATH = "api/app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_turmas():
    conn = get_db_connection()
    cursor = conn.cursor()
    turma = cursor.execute("SELECT * FROM turma").fetchall()
    conn.close()
    return [dict(turma) for turma in turma]

def add_turma(nome, professor_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO turma (nome, professor_id, status) VALUES (?, ?, ?)",
        (nome, professor_id, status)
    )
    conn.commit()
    conn.close()
    

def delete_turma(turma_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM turma WHERE id = ?", (turma_id,))
    conn.commit()
    conn.close()

def update_turma(turma_id, nome, professor_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE turma SET nome = ?, professor_id = ?, status = ? WHERE id = ?", (nome, professor_id, status, turma_id))
    conn.commit()
    conn.close()

def get_turma_by_id(turma_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM turma WHERE id = ?", (turma_id,))
    turma = cursor.fetchone()
    conn.close()
    return turma

def get_turmas_by_professor(professor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM turma WHERE professor_id = ?", (professor_id,))
    turmas = cursor.fetchall()
    conn.close()
    return turmas

def get_turmas_by_usuario(usuario_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM turma
        WHERE professor_id = ?
    """, (usuario_id,))
    turmas = cursor.fetchall()
    conn.close()
    return turmas


def add_aluno_to_turma(turma_id, aluno_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO turma_aluno (turma_id, aluno_id) VALUES (?, ?)",
        (turma_id, aluno_id)
    )
    conn.commit()
    conn.close()

def get_membros_by_turma(turma_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.* FROM usuario u
        JOIN turma_aluno ta ON u.id = ta.aluno_id
        WHERE ta.turma_id = ?
    """, (turma_id,))
    membros = cursor.fetchall()
    conn.close()
    return membros    

def get_alunos_by_turma(turma_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.* FROM usuario u
        JOIN turma_aluno ta ON u.id = ta.aluno_id
        WHERE ta.turma_id = ?
    """, (turma_id,))
    alunos = cursor.fetchall()
    conn.close()
    return alunos

def get_id_by_email(email):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # garante que o fetchone() retorne dict-like
    cursor = conn.cursor()

    # IMPORTANTE: o parâmetro precisa ser uma tupla (email,)
    cursor.execute("SELECT id FROM usuario WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return user['id']
    return None


def get_turmas_by_aluno(aluno_id):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # garante que fetchall() retorne dict-like
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.id, t.nome, t.professor_id
        FROM turma t
        JOIN turma_aluno ta ON t.id = ta.turma_id
        WHERE ta.aluno_id = ?
    """, (aluno_id,))

    turmas = cursor.fetchall()
    conn.close()

    # Converte cada resultado em um dicionário
    return [dict(turma) for turma in turmas]