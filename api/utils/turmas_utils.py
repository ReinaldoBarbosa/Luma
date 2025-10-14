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

