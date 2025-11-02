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

def add_usuario(nome, ra, email, senha, nivel, status, senha_temporaria):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO usuario (nome, ra, email, senha, nivel, status, senha_temporaria)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, ra, email, senha, nivel, status, senha_temporaria))
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

def get_usuario_by_id(user_id):
    conn = get_db_connection()
    usuario = conn.execute("SELECT * FROM usuario WHERE id = ?", (user_id)).fetchone()
    conn.close()

    if usuario:
        return dict(usuario)
    return None

def get_usuario_by_email(email):
    conn = get_db_connection()
    usuario = conn.execute("SELECT * FROM usuario WHERE email = ?", (email,)).fetchone()
    conn.close()

    if usuario:
        return dict(usuario)
    return None

def alterar_senha_usuario(email, nova_senha):
    conn = get_db_connection()
    conn.execute('UPDATE usuario SET senha = ?, senha_temporaria = 0 WHERE email = ?', (nova_senha, email))
    conn.commit()
    conn.close()
