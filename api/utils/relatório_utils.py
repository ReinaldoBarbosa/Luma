import sqlite3

DB_PATH = "api/app.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_relatório():
    conn = get_db_connection()
    cursor = conn.cursor()
    relatório = cursor.execute("SELECT * FROM relatório").fetchall()
    conn.close()
    return [dict(relatório) for relatório in relatório]


def add_relatório(usuario_id, media_geral, total_atividades, data_geracao):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO relatório (usuario_id, media_geral, total_atividades, data_geracao) VALUES (?, ?, ?, ?)",(usuario_id, media_geral, total_atividades, data_geracao))
    conn.commit()
    conn.close()


def delete_relatório(relatório_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM relatório WHERE id = ?", (relatório_id,))
    conn.commit()
    conn.close()


def update_relatório(usuario_id, media_geral, total_atividades, data_geracao):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE relatório SET usuario_id = ?, media_geral = ?, total_atividades = ?, data_geracao = ? WHERE id = ?",(usuario_id, media_geral, total_atividades, data_geracao))
    conn.commit()
    conn.close()


def get_relatório_by_id(relatório_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relatório WHERE id = ?", (relatório_id,))
    relatório = cursor.fetchone()
    conn.close()
    return relatório



