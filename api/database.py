import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Criar tabela de professores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            disciplina TEXT NOT NULL
        )
    ''')

    # Criar tabela de alunos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            ra TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    
    conn.commit()
    conn.close()