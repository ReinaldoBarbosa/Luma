import sqlite3

DB_PATH = "api/app.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_atividade():
    conn = get_db_connection()
    cursor = conn.cursor()
    atividade = cursor.execute("SELECT * FROM atividade").fetchall()
    conn.close()
    return [dict(atividade) for atividade in atividade]


def add_atividade(nome, descricao, link, anexo, turma_id, usuario_id, status, data_criacao, data_entrega):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO atividade (nome, descricao, link, anexo, turma_id, usuario_id,status, data_criacao, data_entrega) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(nome, descricao, link, anexo, turma_id, usuario_id, status, data_criacao, data_entrega))
    conn.commit()
    conn.close()


def delete_atividade(atividade_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM atividade WHERE id = ?", (atividade_id,))
    conn.commit()
    conn.close()


def update_atividade(nome, descricao, link, anexo, turma_id, status, data_criacao, data_entrega):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE atividade SET nome = ?, descricao = ?, link = ?, anexo = ?, turma_id = ? , status = ?, data_criacao = ?, data_entrega = ? WHERE id = ?",
                   (nome, descricao, link, anexo, turma_id, status, data_criacao, data_entrega))
    conn.commit()
    conn.close()


def get_atividades_by_usuario(usuario_id):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM atividade WHERE usuario_id = ?", (usuario_id,))
    linhas = cursor.fetchall()
    conn.close()

    # Converte cada Row em dicionário
    atividades = [dict(linha) for linha in linhas]
    return atividades




def get_atividade_by_professor(atividade_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM atividade WHERE professor_id = ?", (atividade_id,))
    atividade = cursor.fetchall()
    conn.close()
    return atividade

def get_atividade_by_id(atividade_id):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM atividade WHERE id = ?", (atividade_id,))
    linha = cursor.fetchone()
    conn.close()

    if linha:
        return dict(linha)
    return None

def salvar_resposta_atividade(atividade_id, aluno_id, resposta, novo_status="respondida"):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verifica se já existe resposta do aluno para essa atividade
    cursor.execute("""
        SELECT id FROM respostas_atividade
        WHERE atividade_id = ? AND aluno_id = ?
    """, (atividade_id, aluno_id))
    resultado = cursor.fetchone()
    
    if resultado:
        # Atualiza a resposta existente
        cursor.execute("""
            UPDATE respostas_atividade
            SET resposta = ?, data_envio = CURRENT_DATE, status = 'respondida'
            WHERE id = ?
        """, (resposta, resultado['id']))
    else:
        # Insere nova resposta
        cursor.execute("""
            INSERT INTO respostas_atividade (atividade_id, aluno_id, resposta, status)
            VALUES (?, ?, ?, ?)
        """, (atividade_id, aluno_id, resposta, novo_status))
    
    conn.commit()
    conn.close()

def update_nota_resposta(resposta_id, nota, novo_status="corrigida"):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE respostas_atividade
        SET nota = ?, status = ?
        WHERE id = ?
    """, (nota, novo_status, resposta_id))
    
    conn.commit()
    conn.close()


def listar_respostas_atividade(atividade_id):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM respostas_atividade WHERE atividade_id = ?", (atividade_id,))
    linhas = cursor.fetchall()
    conn.close()

    respostas = []
    for linha in linhas:
        r = dict(linha)
        if r["data_envio"]:
            r["data_envio"] = r["data_envio"]  # ou r["data_envio"].strftime("%d/%m/%Y") se for datetime
        respostas.append(r)
    
    return respostas


def correcao_atividade(resposta_id, nota):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE respostas_atividade SET nota = ?, status = 'corrigida' WHERE id = ?", (nota, resposta_id))
    conn.commit()
    conn.close()

def get_respostas_by_atividade(atividade_id):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # JOIN para trazer o nome do aluno
    cursor.execute("""
        SELECT r.aluno_id, u.nome AS aluno_nome, r.resposta, r.nota
        FROM respostas_atividade r
        JOIN usuario u ON r.aluno_id = u.id
        WHERE r.atividade_id = ?
    """, (atividade_id,))

    linhas = cursor.fetchall()
    conn.close()

    respostas = [dict(linha) for linha in linhas]
    return respostas