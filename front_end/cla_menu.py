from api.routes.turma_routes import criar_turma
from front_end.cla_nota import ver_notas_aluno
from front_end.cla_usuario import listar_usuarios, criar_usuario
from front_end.cla_turma import listar_turmas_front, criar_turma_front, listar_turmas_aluno_front
from front_end.cla_relatorio import gerar_relatorio_cli
from front_end.cla_chatbot import iniciar_chatbot as chatbot

def menu_principal(usuario):

    print(f"Usuário logado: {usuario['nome']} - Nível: {usuario['nivel']}")

    nivel =  usuario['nivel']

    if nivel == "professor":
        while True:
            print("\n=== Menu Principal - Professor ===")
            print("1️⃣  Listar Turmas")
            print("2️⃣  Criar Turma")
            print("0️⃣  Sair")
            opc = input("Escolha: ")

            if opc == "1":
               listar_turmas_front(usuario)
            elif opc == "2":
               criar_turma_front(usuario['id'])
            elif opc == "0":
                print("Encerrando o sistema...")
                break
            else:
                print("Opção inválida!")
    elif nivel == "admin":
        while True:
            print("\n=== Menu Principal - Admin ===")
            print("1️⃣  Listar Usuarios")
            print("2️⃣  Criar Usuario")
            print("3️⃣  Gerar relatórios (em breve)")
            print("0️⃣  Sair")

            opc = input("Escolha: ")
            if opc == "1":
                listar_usuarios()
            elif opc == "2":
                criar_usuario()
            elif opc == "3":
                print("📊 Gerar Relatório de Desempenho")
                usuario_id = input("Escreva o ID do usuário para gerar o relatório: ")
                gerar_relatorio_cli(usuario_id)
        
            elif opc == "0":
                print("Encerrando o sistema...")
                break
            else:
                print("Opção inválida!")
    elif nivel == "aluno":
        while True:
            print("\n=== Menu Principal - Aluno ===")
            print("1️⃣  Listar minhas turmas")
            print("2️⃣  Ver notas")
            print("3️⃣  Chatbot")
            print("0️⃣  Sair")
            opc = input("Escolha: ")

            if opc == "1":
              listar_turmas_aluno_front(usuario)
            elif opc == "2":
               ver_notas_aluno(usuario['id'])
               print("Função de ver atividades ainda não implementada!") 
            elif opc == "3":
               chatbot()      
            elif opc == "0":
                print("Encerrando o sistema...")
                break
            else:
                print("Opção inválida!") 
