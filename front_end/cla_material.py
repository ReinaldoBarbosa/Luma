import requests
import os
import keyboard

API_URL = "http://127.0.0.1:5000"

def adicionar_material_front(turma_id):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=" * 40)
        print("📁  Adicionar Novo Material")
        print("=" * 40)
        print(f"Turma ID: {turma_id}")
        print()

        nome = input("Nome do material: ").strip()
        descricao = input("Descrição: ").strip()
        link = input("Link (opcional): ").strip()

        print("\n" + "=" * 40)
        print("1️⃣  Confirmar adição")
        print("2️⃣  Cancelar e voltar")
        print("=" * 40)
        opcao = input("Escolha uma opção: ")

        if opcao == "2":
            print("\n🔙 Voltando ao menu anterior...")
            input("Pressione Enter para continuar...")
            return

        elif opcao == "1":
            if not nome:
                print("\n⚠️  O campo nome é obrigatório.")
                input("Pressione Enter para tentar novamente...")
                continue

            try:
                r = requests.post(f"{API_URL}/material/criar", data={
                    "nome": nome,
                    "descricao": descricao,
                    "link": link if link else None,
                    "anexo":  None,
                    "turma_id": turma_id
                })

                if r.status_code == 201:
                    print("\n✅ Material adicionado com sucesso!")
                else:
                    print("\n❌ Erro ao adicionar material:", r.json().get("error", r.text))

            except Exception as e:
                print("\n❌ Erro ao conectar à API:", e)

            input("\nPressione Enter para voltar ao menu...")
            return

def listar_material_turma(turma_id):
    try:
        while True:
            # 🔹 Buscar materiais atualizados
            r = requests.get(f"{API_URL}/material/turma/{turma_id}")
            if r.status_code != 200:
                print("❌ Erro ao listar materiais:", r.json().get("error", r.text))
                input("\nPressione Enter para voltar...")
                return

            materiais = r.json().get("materiais", [])
            if not materiais:
                print("\n📄 Nenhum material encontrado para esta turma.")
                input("\nPressione Enter para voltar...")
                return

            index = 0

            # 🔹 Loop de navegação
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("📚 Materiais da Turma")
                print("=" * 50)

                for i, m in enumerate(materiais):
                    marcador = ">" if i == index else " "
                    print(f"{marcador} ID {m['id']} - {m['nome']}")
                    print(f"   Descrição: {m.get('descricao', '---')[:60]}...\n")

                print("\n⬆️ / ⬇️ para navegar | Enter para ver conteúdo | ESC para voltar")

                event = keyboard.read_event(suppress=True)
                if event.event_type != "down":
                    continue

                key = event.name
                if key == "up":
                    index = (index - 1) % len(materiais)
                elif key == "down":
                    index = (index + 1) % len(materiais)
                elif key == "enter":
                    material = materiais[index]
                    ver_material_detalhado(material['id'])
                    break  # volta e recarrega a lista após ver o detalhe
                elif key == "esc":
                    return

    except Exception as e:
        print("\n❌ Erro ao conectar à API:", e)
        input("\nPressione Enter para voltar...")  
            
def ver_material_detalhado(material_id):
    try:
        r = requests.get(f"{API_URL}/material/turma/{material_id}")
        if r.status_code != 200:
            print("\n❌ Erro ao buscar materiais:", r.json().get("error", r.text))
            input("\nPressione Enter para voltar...")
            return

        materiais = r.json().get("materiais", [])
        if not materiais:
            print("\n⚠️ Nenhum material encontrado para esta turma.")
            input("\nPressione Enter para voltar...")
            return

        index = 0

        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print("=" * 50)
            print("📚 Materiais da Turma")
            print("=" * 50)

            for i, mat in enumerate(materiais):
                marcador = ">" if i == index else " "
                print(f"{marcador} {mat['nome']} ")

            print("\n⬆️ / ⬇️ para navegar | Enter para ver detalhes | ESC para voltar")

            import keyboard
            event = keyboard.read_event(suppress=True)
            if event.event_type != "down":
                continue

            key = event.name
            if key == "up":
                index = (index - 1) % len(materiais)
            elif key == "down":
                index = (index + 1) % len(materiais)
            elif key == "enter":
                material = materiais[index]
                os.system("cls" if os.name == "nt" else "clear")
                print("=" * 50)
                print(f"📘 Título: {material['nome']}")
                print(f"📝 Descrição: {material.get('descricao', '---')}")
                print(f"📄 Link:\n{material.get('link', '---')}")
                print("=" * 50)
                input("\nPressione Enter para voltar à lista de materiais...")
            elif key == "esc":
                return

    except Exception as e:
        print("\n❌ Erro ao conectar à API:", e)
        input("\nPressione Enter para voltar...")