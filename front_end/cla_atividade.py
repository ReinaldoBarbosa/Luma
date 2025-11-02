import requests
import os

API_URL = "http://127.0.0.1:5000"  # Altere se necessário

def criar_atividade_front(turma_id, usuario_id):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=" * 40)
        print("📘  Criar nova atividade")
        print("=" * 40)
        print(f"Turma ID: {turma_id}")
        print()

        nome = input("Título da atividade: ").strip()
        descricao = input("Descrição: ").strip()
        link = input("Link (opcional): ").strip()
        anexo = input("Anexo (opcional): ").strip()
        data_entrega = input("Prazo (YYYY-MM-DD): ").strip()
        usuario_id = usuario_id

        print("\n" + "=" * 40)
        print("1️⃣  Confirmar criação")
        print("2️⃣  Cancelar e voltar")
        print("=" * 40)
        opcao = input("Escolha uma opção: ")

        if opcao == "2":
            print("\n🔙 Voltando ao menu anterior...")
            input("Pressione Enter para continuar...")
            return

        elif opcao == "1":
            if not nome or not descricao or not data_entrega:
                print("\n⚠️  Campos obrigatórios: título, descrição e prazo.")
                input("Pressione Enter para tentar novamente...")
                continue

            try:
                r = requests.post(f"{API_URL}/atividade/criar", json={
                    "turma_id": turma_id,
                    "nome": nome,
                    "descricao": descricao,
                    "link": link if link else None,
                    "anexo": anexo if anexo else None,
                    "data_entrega": data_entrega,
                    "usuario_id": usuario_id,
                    "status": "em_andamento"
                })

                if r.status_code == 201:
                    print("\n✅ Atividade criada com sucesso!")
                else:
                    print("\n❌ Erro ao criar atividade:", r.json().get("error", r.text))

            except Exception as e:
                print("\n❌ Erro ao conectar à API:", e)

            input("\nPressione Enter para voltar ao menu...")
            return
        else:
            print("\n⚠️ Opção inválida.")
            input("Pressione Enter para continuar...")

def ver_detalhes_atividade(atividade, usuario_nivel,  professor_id, aluno_id):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"📋 Detalhes da Atividade\n{'='*40}")
        print(f"📘 Título: {atividade.get('nome', '---')}")
        print(f"📝 Descrição: {atividade.get('descricao', '---')}")
        print(f"📅 Prazo: {atividade.get('data_entrega', '---')}")
        print(f"🔗 Link: {atividade.get('link', '---')}")
        print(f"📎 Anexo: {atividade.get('anexo', '---')}")
        print(f"📆 Criada em: {atividade.get('data_criacao', '---')}")
        print(f"📊 Status: {atividade.get('status', 'Em andamento')}")
        print("="*40)

        if usuario_nivel == "aluno":
            print("1️⃣  Responder atividade")
            print("2️⃣  Voltar")
            escolha = input("\nEscolha: ")
        elif usuario_nivel == "professor":
            print("1️⃣  Corrigir respostas")
            print("2️⃣  Voltar")
            escolha = input("\nEscolha: ")

        if escolha == "1":
            if usuario_nivel == "professor":
                from front_end.cla_nota import corrigir_respostas_front
                corrigir_respostas_front(atividade.get("turma_id"), atividade.get("id"), professor_id)
            else:
                from front_end.cla_atividade import responder_atividade_front
                responder_atividade_front(atividade["id"], aluno_id, atividade.get("turma_id"))
            input("\n✅ Ação concluída. Pressione Enter para continuar...")
        elif escolha == "2":
            break
        else:
            input("⚠️ Opção inválida. Pressione Enter para continuar...")



# === RESPONDER ATIVIDADE ===
def responder_atividade_front(atividade_id, aluno_id, turma_id):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("✍️  Responder atividade")
    print("="*40)

    resposta = input("Digite sua resposta (ou link para arquivo): ").strip()

    if not resposta:
        print("\n⚠️ A resposta não pode estar vazia.")
        input("Pressione Enter para voltar...")
        return

    try:
        r = requests.post(f"{API_URL}/atividade/responder", json={
            "atividade_id": atividade_id,
            "aluno_id": aluno_id,
            "resposta": resposta
        })

        if r.status_code == 200:
            print("\n✅ Resposta enviada com sucesso!")
        else:
            print("\n❌ Erro ao enviar resposta:", r.text)

    except Exception as e:
        print("\n❌ Erro ao conectar à API:", e)

    input("\nPressione Enter para voltar...")

def listar_minhas_atividades(usuario_id):
    try:
        r = requests.get(f"{API_URL}/atividade/minhas/{usuario_id}")
        if r.status_code == 200:
            atividades = r.json()
            if not atividades:
                print("\n⚠️ Nenhuma atividade encontrada.")
            else:
                print("\n📋 Minhas Atividades:")
                for a in atividades:
                    print(f"  ID {a['id']} - {a['nome']} - Status: {a['status']}")
                escolha = input("\nDigite o ID da atividade para ver detalhes (ou '0' para voltar): ")
                if escolha != "0":
                    atividade_selecionada = next((x for x in atividades if str(x['id']) == escolha), None)
                    if atividade_selecionada:
                        ver_detalhes_atividade(atividade_selecionada)
                    else:
                        input("⚠️ Atividade não encontrada. Pressione Enter para continuar...")
        else:
            print("Erro ao listar minhas atividades:", r.json())
    except Exception as e:
        print("❌ Erro ao conectar à API:", e)