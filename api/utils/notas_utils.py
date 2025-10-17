import sqlite3

DB_PATH = "api/app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_notas():
    conn = get_db_connection()
    notas = conn.execute('SELECT * FROM notas').fetchall()
    conn.close()
    return [dict(notas) for notas in notas]

def add_notas(usuario_id, atividade_id, nota):
    conn = get_db_connection()
    conn.execute('INSERT INTO notas (usuario_id, atividade_id, nota) VALUES (?, ?, ?)', (usuario_id, atividade_id, nota))
    conn.commit()
    conn.close()

def delete_notas(notas_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM notas WHERE id = ?', (notas_id,))
    conn.commit()
    conn.close()

def update_notas(usuario_id, atividade_id, nota):
    conn = get_db_connection()
    conn.execute('UPDATE notas SET usuario_id = ?, atividade_id = ?, nota = ?, WHERE id = ?', (usuario_id, atividade_id, nota))
    conn.commit()
    conn.close()

def get_notas_by_id(notas_id):
    conn = get_db_connection()
    notas = conn.execute('SELECT * FROM notas WHERE id = ?', (notas_id,)).fetchone()
    conn.close()
    return dict(notas) if notas else None