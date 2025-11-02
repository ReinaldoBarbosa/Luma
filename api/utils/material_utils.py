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
    return [dict(mat) for mat in material]

def add_material(nome, descricao, link, anexo, turma_id, status):
    conn = get_db_connection()
    conn.execute('INSERT INTO material (nome, descricao, link, anexo, turma_id, status) VALUES (?, ?, ?, ?, ?, ?)', (nome, descricao, link, anexo, turma_id, status))
    conn.commit()
    conn.close()

def delete_material(material_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM material WHERE id = ?', (material_id,))
    conn.commit()
    conn.close()

def update_material(nome, descricao, link, anexo, status, material_id):
    conn = get_db_connection()
    conn.execute('UPDATE material SET nome = ?, descricao = ?, link = ?, anexo = ?, status = ? WHERE id = ?', (nome, descricao, link, anexo, status, material_id))
    conn.commit()
    conn.close()

# listar todos os materiais de uma turma
def get_materiais_by_turma(turma_id):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, descricao, link
        FROM material
        WHERE turma_id = ?
    """, (turma_id,))
    materiais = cursor.fetchall()
    conn.close()
    return [dict(m) for m in materiais]

# obter conteudo de um material
def get_material_by_id(material_id):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, descricao, link
        FROM material
        WHERE id = ?
    """, (material_id,))
    material = cursor.fetchone()
    conn.close()
    return dict(material) if material else None
