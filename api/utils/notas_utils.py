import sqlite3

DB_PATH = "api/app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# 🔹 Listar todas as notas
def get_all_notas():
    conn = get_db_connection()
    notas = conn.execute('SELECT * FROM nota').fetchall()
    conn.close()
    return [dict(nota) for nota in notas]


# 🔹 Adicionar uma nota (lançada pelo professor)
def add_nota(usuario_id, atividade_id, nota):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nota (usuario_id, atividade_id, nota)
        VALUES (?, ?, ?)
    ''', (usuario_id, atividade_id, nota))
    conn.commit()
    conn.close()


# 🔹 Excluir uma nota
def delete_nota(nota_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM nota WHERE id = ?', (nota_id,))
    conn.commit()
    conn.close()


# 🔹 Atualizar nota existente
def update_nota(nota_id, usuario_id, atividade_id, nota):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nota
        SET usuario_id = ?, atividade_id = ?, nota = ?
        WHERE id = ?
    ''', (usuario_id, atividade_id, nota, nota_id))
    conn.commit()
    conn.close()


# 🔹 Buscar nota por ID
def get_nota_by_id(nota_id):
    conn = get_db_connection()
    nota = conn.execute('SELECT * FROM nota WHERE id = ?', (nota_id,)).fetchone()
    conn.close()
    return dict(nota) if nota else None


# 🔹 Buscar notas por usuário (aluno)
def get_notas_by_usuario(usuario_id):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # garante que fetchall retorne dict-like
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT n.nota, a.nome AS atividade_nome
        FROM nota n
        JOIN atividade a ON n.atividade_id = a.id
        WHERE n.usuario_id = ?
    """, (usuario_id,))
    
    notas = cursor.fetchall()
    conn.close()
    
    return [dict(n) for n in notas]



# 🔹 Buscar notas por turma (para o professor ver todas as notas)
def get_notas_by_turma(turma_id):
    conn = get_db_connection()
    notas = conn.execute('''
        SELECT u.nome AS aluno, a.titulo AS atividade, n.nota
        FROM nota n
        JOIN usuario u ON u.id = n.usuario_id
        JOIN atividade a ON a.id = n.atividade_id
        WHERE a.turma_id = ?
    ''', (turma_id,)).fetchall()
    conn.close()
    return [dict(nota) for nota in notas]

