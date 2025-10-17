import sqlite3

DB_PATH = "api/app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_material():
    conn = get_db_connection()
    material = conn.execute('SELECT * FROM material').fetchall()
    conn.close()
    return [dict(material) for material in material]

def add_material(nome, ra, email, senha, nivel, status):
    conn = get_db_connection()
    conn.execute('INSERT INTO material (nome, ra, email, senha, nivel, status) VALUES (?, ?, ?, ?, ?, ?)', (nome, ra, email, senha, nivel, status))
    conn.commit()
    conn.close()

def delete_material(material_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM material WHERE id = ?', (material_id,))
    conn.commit()
    conn.close()

def update_material(nome, ra, email, senha, nivel, usuario_id):
    conn = get_db_connection()
    conn.execute('UPDATE usuario SET nome = ?, ra = ?, email = ?, senha = ?, nivel = ? WHERE id = ?', (nome, ra, email, senha, nivel, usuario_id))
    conn.commit()
    conn.close()

def get_material_by_id(material_id):
    conn = get_db_connection()
    material = conn.execute('SELECT * FROM material WHERE id = ?', (material_id,)).fetchone()
    conn.close()
    return dict(material) if material else None