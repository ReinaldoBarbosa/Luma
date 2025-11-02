import sqlite3
import os
import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # ==========================
    # 📁 CRIAÇÃO DAS TABELAS
    # ==========================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            ra TEXT UNIQUE,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            nivel TEXT CHECK(nivel IN ('aluno', 'professor', 'admin')) NOT NULL,
            status TEXT DEFAULT 'ativo',
            senha_temporaria INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS turma (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            professor_id INTEGER NOT NULL,
            status TEXT DEFAULT 'ativo',
            FOREIGN KEY (professor_id) REFERENCES usuario (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS atividade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            link TEXT,
            anexo TEXT,
            turma_id INTEGER NOT NULL,
            usuario_id INTEGER,  -- 👈 adiciona o criador
            status TEXT CHECK(status IN ('em_andamento', 'respondida', 'corrigida', 'finalizada')) DEFAULT 'em_andamento',
            data_criacao DATE DEFAULT CURRENT_DATE,
            data_entrega DATE,
            FOREIGN KEY (turma_id) REFERENCES turma(id),
            FOREIGN KEY (usuario_id) REFERENCES usuario(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS material (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            link TEXT,
            anexo TEXT,
            turma_id INTEGER NOT NULL,
            status TEXT CHECK(status IN ('ativo', 'inativo')) DEFAULT 'ativo',
            FOREIGN KEY (turma_id) REFERENCES turma(id)
        )
    ''')

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

    # ==========================
    # 👑 CRIAR ADMIN PADRÃO
    # ==========================
    cursor.execute("SELECT * FROM usuario WHERE nivel = 'admin'")
    admin_existente = cursor.fetchone()

    if not admin_existente:
        nome = "Admin"
        ra = None
        email = "admin@admin.unip.com"
        senha_temp = "rei123"
        senha_hash = hashlib.sha256(senha_temp.encode()).hexdigest()
        nivel = "admin"
        status = "ativo"
        senha_temporaria = 1

        cursor.execute('''
            INSERT INTO usuario (nome, ra, email, senha, nivel, status, senha_temporaria)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, ra, email, senha_hash, nivel, status, senha_temporaria))
        conn.commit()
        print(f"✅ Admin criado com sucesso! Email: {email}, Senha temporária: {senha_temp}")

    conn.close()
