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


def add_relatório(nome, professor_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO relatório (nome, professor_id, status) VALUES (?, ?, ?)",
        (nome, professor_id, status)
    )
    conn.commit()
    conn.close()


def delete_relatório(relatório_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM relatório WHERE id = ?", (relatório_id,))
    conn.commit()
    conn.close()


def update_relatório(relatório_id, nome, professor_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE relatório SET nome = ?, professor_id = ?, status = ? WHERE id = ?",
                   (nome, professor_id, status, relatório_id))
    conn.commit()
    conn.close()


def get_relatório_by_id(relatório_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relatório WHERE id = ?", (relatório_id,))
    relatório = cursor.fetchone()
    conn.close()
    return relatório


def get_relatório_by_professor(professor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relatório WHERE professor_id = ?", (professor_id,))
    relatório = cursor.fetchall()
    conn.close()
    return relatório
