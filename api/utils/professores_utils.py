import sqlite3

DB_PATH = "api/app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_professores():
    conn = get_db_connection()
    professores = conn.execute('SELECT * FROM professores').fetchall()
    conn.close()
    return [dict(professor) for professor in professores]

def add_professor(nome, disciplina):
    conn = get_db_connection()
    conn.execute('INSERT INTO professores (nome, disciplina) VALUES (?, ?)', (nome, disciplina))
    conn.commit()
    conn.close()

def delete_professor(professor_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM professores WHERE id = ?', (professor_id,))
    conn.commit()
    conn.close()

def update_professor(professor_id, nome, disciplina):
    conn = get_db_connection()
    conn.execute('UPDATE professores SET nome = ?, disciplina = ? WHERE id = ?', (nome, disciplina, professor_id))
    conn.commit()
    conn.close()    