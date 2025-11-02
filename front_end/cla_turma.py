from operator import index
import requests
import os
import keyboard

from cla_atividade import criar_atividade_front, ver_detalhes_atividade
from cla_material import adicionar_material_front, listar_material_turma

API_URL = "http://127.0.0.1:5000"

def criar_turma_front(usuario_id):
    nome = input("Nome da turma: ")

    try:
        r = requests.post(f"{API_URL}/turma/criar", json={"nome": nome,"professor_id": usuario_id})
        print(r.json().get("message", "Erro desconhecido"))
    except Exception as e:
        print("❌ Erro ao conectar à API:", e) 

def listar_turmas_front(usuario):
    usuario_id = usuario['id']
    try:
        r = requests.get(f"{API_URL}/turma/minhas/{usuario_id}")
        if r.status_code != 200:
            print("❌ Erro ao listar minhas turmas:", r.json())
            return
        
        turmas = r.json()
        if not turmas:
            print("\n⚠️ Nenhuma turma encontrada.")
            input("\nPressione Enter para voltar...")
            return

        index = 0

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("📋 Minhas Turmas (use ↑ ↓ e Enter):\n")

            for i, t in enumerate(turmas):
                if i == index:
                    print(f"> {t['nome']}  (ID: {t['id']})")
                else:
                    print(f"  {t['nome']}  (ID: {t['id']})")

            print("\n⬆️ / ⬇️ para navegar | Enter para acessar | ESC para sair")

            key = keyboard.read_event(suppress=True).name

            if key == "up":
                index = (index - 1) % len(turmas)
            elif key == "down":
                index = (index + 1) % len(turmas)
            elif key == "enter":
                turma_selecionada = turmas[index]
                acessar_turma_front(turma_selecionada, usuario)
            elif key == "esc":
                break

    except Exception as e:
        print("❌ Erro ao conectar à API:", e)
        input("\nPressione Enter para continuar...")

def acessar_turma_front(turma, usuario):
    opcoes = [
        "📚 Ver Atividades",
        "👥 Ver Membros",
        "📁 Ver Materiais",
        "📝 Criar Nova Atividade",
        "➕ Adicionar Material",
        "➕ Adicionar Membro",
        "⬅️ Voltar"
    ]

    index = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"=== Turma: {turma['nome']} ===\n")

        for i, opcao in enumerate(opcoes):
            if i == index:
                print(f"> {opcao}")  # opção selecionada
            else:
                print(f"  {opcao}")

        print("\n⬆️ / ⬇️ para navegar | Enter para selecionar | ESC para sair")

        event = keyboard.read_event(suppress=True)
        if event.event_type != "down":
            continue  # ignora keyup

        key = event.name

        if key == "up":
            index = (index - 1) % len(opcoes)
        elif key == "down":
            index = (index + 1) % len(opcoes)
        elif key == "enter":
            opcao_selecionada = opcoes[index]
            os.system('cls' if os.name == 'nt' else 'clear')

            if "Ver Atividades" in opcao_selecionada:
                print(f"📚 Atividades da turma: {turma['nome']}\n")

                if not turma.get('atividades'):
                    ver_atividades(turma['professor_id'], usuario)
                else:
                    for a in turma['atividades']:
                        print(f"📝 {a['titulo']} - Status: {a['status']} (ID: {a['id']})")

                input("\nPressione Enter para voltar...")

            elif "Ver Membros" in opcao_selecionada:
                print(f"👥 Membros da turma: {turma['nome']}\n")
                membros = get_membros_by_turma(turma['id'])
                for m in membros:
                    print(f" - {m['nome']} (ID: {m['id']})")
                input("\nPressione Enter para voltar...")

            elif "Ver Materiais" in opcao_selecionada:
                listar_material_turma(turma['id'])

            elif "Criar Nova Atividade" in opcao_selecionada:
                criar_atividade_front(turma['id'], turma['professor_id'])
                
            elif "Adicionar Material" in opcao_selecionada:
                adicionar_material_front(turma['id'])    

            elif "Adicionar Membro" in opcao_selecionada:
                print(f"➕ Adicionar membro à turma: {turma['nome']}")
                email = input("Email do novo membro: ")
                add_membro_to_turma(turma['id'], email)
                input("\nPressione Enter para voltar...")

            elif "Voltar" in opcao_selecionada:
                break

        elif key == "esc":
            break

def ver_atividades(usuario_id, usuario):
    try:
        while True:
            # Buscar atividades sempre atualizado
            r = requests.get(f"{API_URL}/atividade/minhas/{usuario_id}")
            if r.status_code != 200:
                print("❌ Erro ao listar minhas atividades:", r.json())
                return
            
            atividades = r.json()
            if not atividades:
                print("📋 Nenhuma atividade encontrada.")
                return
            
            index = 0

            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n📋 Minhas Atividades:")

                for i, t in enumerate(atividades):
                    marcador = ">" if i == index else " "
                    print(f"{marcador} ID {t['id']} - {t['nome']} - Descrição: {t.get('descricao', '---')} - Criada: {t.get('data_criacao', '---')} - Status: {t.get('status', 'Em andamento')}")

                print("\n⬆️ / ⬇️ para navegar | Enter para acessar | ESC para sair")

                event = keyboard.read_event(suppress=True)
                if event.event_type != "down":
                    continue  # só considera tecla pressionada

                key = event.name
                if key == "up":
                    index = (index - 1) % len(atividades)
                elif key == "down":
                    index = (index + 1) % len(atividades)
                elif key == "enter":
                    atividade_selecionada = atividades[index]
                    ver_detalhes_atividade(atividade_selecionada, usuario['nivel'], usuario_id, usuario['id'] )
                    break  # volta para recarregar atividades
                elif key == "esc":
                    return  # sai da função

    except Exception as e:
        print("❌ Erro ao conectar à API:", e)


def get_membros_by_turma(turma_id):
    try:
        r = requests.get(f"{API_URL}/turma/listar/membros/{turma_id}")
        if r.status_code != 200:
            print("❌ Erro ao listar membros da turma:", r.json())
            return []
        
        membros = r.json()
        return membros

    except Exception as e:
        print("❌ Erro ao conectar à API:", e)
        return []
        
def add_membro_to_turma(turma_id, email):
    try:
        r = requests.post(f"{API_URL}/turma/add/aluno/{turma_id}", json={"email": email})
        print(r.json().get("message", "Erro desconhecido"))
    except Exception as e:
        print("❌ Erro ao conectar à API:", e)        


# Aluno
def listar_turmas_aluno_front(usuario):
    usuario_id = usuario['id']
    try:
        r = requests.get(f"{API_URL}/turma/alunos/minhas/{usuario_id}")
        if r.status_code != 200:
            print("❌ Erro ao listar minhas turmas:", r.json())
            return
        
        turmas = r.json()
        if not turmas:
            print("\n⚠️ Nenhuma turma encontrada.")
            input("\nPressione Enter para voltar...")
            return
        
        index = 0

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("📋 Minhas Turmas (use ↑ ↓ e Enter):\n")

            for i, t in enumerate(turmas):
                if i == index:
                    print(f"> {t['nome']}  (ID: {t['id']})")
                else:
                    print(f"  {t['nome']}  (ID: {t['id']})")

            print("\n⬆️ / ⬇️ para navegar | Enter para acessar | ESC para sair")

            key = keyboard.read_event(suppress=True).name

            if key == "up":
                index = (index - 1) % len(turmas)
            elif key == "down":
                index = (index + 1) % len(turmas)
            elif key == "enter":
                turma_selecionada = turmas[index]
                acessar_turma_aluno(turma_selecionada, usuario)
            elif key == "esc":
                break

    except Exception as e:
        print("❌ Erro ao conectar à API:", e)
        input("\nPressione Enter para continuar...")

def acessar_turma_aluno(turma, usuario):
    opcoes = [
        "📚 Ver Atividades",
        "👥 Ver Membros",
        "📁 Ver Materiais",
        "⬅️ Voltar"
    ]

    index = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"=== Turma: {turma['nome']} ===\n")

        for i, opcao in enumerate(opcoes):
            if i == index:
                print(f"> {opcao}")  # opção selecionada
            else:
                print(f"  {opcao}")

        print("\n⬆️ / ⬇️ para navegar | Enter para selecionar | ESC para sair")

        event = keyboard.read_event(suppress=True)
        if event.event_type != "down":
            continue  # ignora keyup

        key = event.name

        if key == "up":
            index = (index - 1) % len(opcoes)
        elif key == "down":
            index = (index + 1) % len(opcoes)
        elif key == "enter":
            opcao_selecionada = opcoes[index]
            os.system('cls' if os.name == 'nt' else 'clear')

            if "Ver Atividades" in opcao_selecionada:
                print(f"📚 Atividades da turma: {turma['nome']}\n")

                if not turma.get('atividades'):
                    ver_atividades(turma['professor_id'], usuario)
                else:
                    for a in turma['atividades']:
                        print(f"📝 {a['titulo']} - Status: {a['status']} (ID: {a['id']})")

                input("\nPressione Enter para voltar...")

            elif "Ver Membros" in opcao_selecionada:
                print(f"👥 Membros da turma: {turma['nome']}\n")
                membros = get_membros_by_turma(turma['id'])
                for m in membros:
                    print(f" - {m['nome']} (ID: {m['id']})")
                input("\nPressione Enter para voltar...")
            elif "Ver Materiais" in opcao_selecionada:
                listar_material_turma(turma['id'])
            elif "Voltar" in opcao_selecionada:
                break

        elif key == "esc":
            break
