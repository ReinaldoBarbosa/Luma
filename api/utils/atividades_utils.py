import sqlite3

DB_PATH = "api/app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_atividades():
    conn = get_db_connection()
    atividades = conn.execute('SELECT * FROM usuario').fetchall()
    conn.close()
    return [dict(atividades) for atividades in atividades]

def add_atividades(nome, ra, email, senha, nivel, status):
    conn = get_db_connection()
    conn.execute('INSERT INTO usuario (nome, ra, email, senha, nivel, status) VALUES (?, ?, ?, ?, ?, ?)', (nome, ra, email, senha, nivel, status))
    conn.commit()
    conn.close()

def delete_atividades(atividades_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM atividades WHERE id = ?', (atividades_id,))
    conn.commit()
    conn.close()

def update_atividade(nome, ra, email, senha, nivel, usuario_id):
    conn = get_db_connection()
    conn.execute('UPDATE atividades SET nome = ?, ra = ?, email = ?, senha = ?, nivel = ? WHERE id = ?', (nome, ra, email, senha, nivel, usuario_id))
    conn.commit()
    conn.close()

def get_atividades_by_id(atividades_id):
    conn = get_db_connection()
    atividades = conn.execute('SELECT * FROM atividades WHERE id = ?', (atividades_id,)).fetchone()
    conn.close()
    return dict(atividades) if atividades else None