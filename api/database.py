import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Criar tabela de Usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            ra TEXT UNIQUE,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            nivel TEXT CHECK(nivel IN ('aluno', 'professor', 'admin')) NOT NULL,
            status TEXT DEFAULT 'ativo'
        )
    ''')

    # Criar tabela de Turmas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS turma (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            professor_id INTEGER NOT NULL,
            status TEXT DEFAULT 'ativo',
            FOREIGN KEY (professor_id) REFERENCES usuario (id)
        )
    ''')

     # Criar tabela de Atividades
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS atividade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            link TEXT,
            anexo TEXT,
            turma_id INTEGER NOT NULL,
            status TEXT CHECK(status IN ('em_andamento', 'respondida', 'corrigida', 'finalizada')) DEFAULT 'em_andamento',
            data_criacao DATE DEFAULT CURRENT_DATE,
            data_entrega DATE,
            FOREIGN KEY (turma_id) REFERENCES turma(id)
        )
    ''')

     # Criar tabela de Notas
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS nota (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            atividade_id INTEGER NOT NULL,
            nota REAL CHECK(nota >= 0 AND nota <= 10),
            FOREIGN KEY (usuario_id) REFERENCES usuario (id),
            FOREIGN KEY (atividade_id) REFERENCES atividade (id)
        )
    ''')

    # Criar tabela de Relatórios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relatorios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            media_geral REAL,
            total_atividades INTEGER,
            data_geracao DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (usuario_id) REFERENCES usuario (id)
        )
    ''')
    
    # Criar tabela de Turma_Aluno (relação muitos-para-muitos entre turmas e alunos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS turma_aluno (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            turma_id INTEGER NOT NULL,
            aluno_id INTEGER NOT NULL,
            data_ingresso DATE DEFAULT CURRENT_DATE,
            status TEXT DEFAULT 'ativo',
            FOREIGN KEY (turma_id) REFERENCES turma(id),
            FOREIGN KEY (aluno_id) REFERENCES usuario(id)
        )
    ''')

    # Criar tabela de Respostas de Atividades
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respostas_atividade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            atividade_id INTEGER NOT NULL,
            aluno_id INTEGER NOT NULL,
            resposta TEXT,
            data_envio DATE DEFAULT CURRENT_DATE,
            status TEXT CHECK(status IN ('pendente', 'respondida', 'corrigida')) DEFAULT 'pendente',
            nota REAL CHECK(nota >= 0 AND nota <= 10),
            FOREIGN KEY (atividade_id) REFERENCES atividade(id),
            FOREIGN KEY (aluno_id) REFERENCES usuario(id)
        )
    ''')

    
    conn.commit()
    conn.close()