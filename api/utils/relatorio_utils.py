import sqlite3
from datetime import datetime
DB_PATH = "api/app.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def gerar_relatorio(usuario_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Calcula média e quantidade de atividades
    cursor.execute("""
        SELECT 
            AVG(nota) AS media_geral,
            COUNT(*) AS total_atividades
        FROM nota
        WHERE usuario_id = ?
    """, (usuario_id,))
    
    resultado = cursor.fetchone()
    media_geral = resultado["media_geral"] or 0
    total_atividades = resultado["total_atividades"] or 0

    # Insere o relatório no banco
    cursor.execute("""
        INSERT INTO relatorios (usuario_id, media_geral, total_atividades, data_geracao)
        VALUES (?, ?, ?, ?)
    """, (usuario_id, media_geral, total_atividades, datetime.now().date()))

    conn.commit()
    conn.close()

    return {
        "usuario_id": usuario_id,
        "media_geral": round(media_geral, 2),
        "total_atividades": total_atividades,
        "data_geracao": str(datetime.now().date())
    }
