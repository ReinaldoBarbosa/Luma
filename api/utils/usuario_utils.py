import sqlite3

DB_PATH = "api/app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_usuario():
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuario').fetchall()
    conn.close()
    return [dict(usuario) for usuario in usuario]

def add_usuario(nome, ra, email, senha, nivel, status):
    conn = get_db_connection()
    conn.execute('INSERT INTO usuario (nome, ra, email, senha, nivel, status) VALUES (?, ?, ?, ?, ?, ?)', (nome, ra, email, senha, nivel, status))
    conn.commit()
    conn.close()

def delete_usuario(usuario_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM usuario WHERE id = ?', (usuario_id,))
    conn.commit()
    conn.close()

def update_usuario(nome, ra, email, senha, nivel, usuario_id):
    conn = get_db_connection()
    conn.execute('UPDATE usuario SET nome = ?, ra = ?, email = ?, senha = ?, nivel = ? WHERE id = ?', (nome, ra, email, senha, nivel, usuario_id))
    conn.commit()
    conn.close()    

def get_usuario_by_id(usuario_id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuario WHERE id = ?', (usuario_id,)).fetchone()
    conn.close()
    return dict(usuario) if usuario else None
