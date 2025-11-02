import requests

API_URL = "http://127.0.0.1:5000"

def listar_usuarios():
    try:
        r = requests.get(f"{API_URL}/usuario/listar")
        print(r)
        if r.status_code == 200:
            print("\n📋 Usuarios cadastrados:")
            for p in r.json():
                print(f"  ID {p['id']} - {p['nome']} - ({p['ra']}) - {p['email']} - Nível: {p['nivel']} - Status: {p['status']}")
        else:
            print("Erro ao listar usuarios:", r.json())
    except Exception as e:
        print("❌ Erro ao conectar à API:", e)

def criar_usuario():

    while True:
        print("\n=== Sistema de Cadastro ===")
        print("1️⃣  Professor")
        print("2️⃣  Aluno")
        print("3️⃣  Admin")
        print("0️⃣  Sair")
        opc = input("Escolha: ")

        if opc == "1":
            nivel = "professor"
            break
        elif opc == "2":
            nivel = "aluno"
            break
        elif opc == "3":
            nivel = "admin"
            break
        elif opc == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida!")

    nome = input("Nome do usuario: ")

    try:
        r = requests.post(f"{API_URL}/usuario/criar", json={"nome": nome,"nivel": nivel})
        print(r.json().get("message", "Erro desconhecido"))
    except Exception as e:
        print("❌ Erro ao conectar à API:", e)

