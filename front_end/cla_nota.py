import requests
import os
import keyboard

API_URL = "http://127.0.0.1:5000"

def corrigir_respostas_front(turma_id, atividade_id, professor_id):
    try:
        # Buscar respostas já enviadas
        r = requests.get(f"{API_URL}/atividade/respostas/{atividade_id}")
        if r.status_code != 200:
            print("\n❌ Erro ao buscar respostas:", r.json().get("error", r.text))
            input("Pressione Enter para voltar...")
            return

        respostas = r.json().get("respostas", [])
        if not respostas:
            print("\n⚠️ Nenhuma resposta encontrada para esta atividade.")
            input("Pressione Enter para voltar...")
            return

        index = 0

        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print("=" * 50)
            print("📝  Corrigir Respostas da Atividade")
            print("=" * 50)

            for i, resposta in enumerate(respostas):
                marcador = ">" if i == index else " "
                nota_atual = resposta.get("nota", "---")
                print(f"{marcador} Aluno: {resposta['aluno_nome']} | Nota: {nota_atual} | Resposta: {resposta['resposta'][:50]}...")

            print("\n⬆️ / ⬇️ para navegar | Enter para corrigir | ESC para voltar")

            event = keyboard.read_event(suppress=True)
            if event.event_type != "down":
                continue

            key = event.name
            if key == "up":
                index = (index - 1) % len(respostas)
            elif key == "down":
                index = (index + 1) % len(respostas)
            elif key == "enter":
                # Corrigir a resposta selecionada
                selected = respostas[index]
                print(f"\nAluno ID: {selected['aluno_id']}")
                print(f"Resposta completa:\n{selected['resposta']}\n")
                nota = input("Digite a nota (0-10) ou deixe em branco para pular: ").strip()
                if nota:
                    try:
                        nota_valor = float(nota)
                        if 0 <= nota_valor <= 10:
                            salvar_nota(selected['aluno_id'], atividade_id, nota_valor, professor_id)
                            print("✅ Nota salva com sucesso!")
                            # Atualiza localmente para mostrar no menu
                            selected['nota'] = nota_valor
                        else:
                            print("❌ Nota inválida. Deve ser entre 0 e 10.")
                    except ValueError:
                        print("❌ Entrada inválida. Por favor, insira um número válido.")
                else:
                    print("⏭️ Pulando esta resposta.")
                input("\nPressione Enter para continuar...")
            elif key == "esc":
                return

    except Exception as e:
        print("\n❌ Erro ao conectar à API:", e)
        input("Pressione Enter para voltar...")

def salvar_nota(aluno_id, atividade_id, nota, professor_id):
    try:
        r = requests.post(f"{API_URL}/notas/lancar", json={
            "atividade_id": atividade_id,
            "aluno_id": aluno_id,
            "nota": nota,
            "professor_id": professor_id
        })

        if r.status_code == 200:
            return True
        else:
            print("❌ Erro ao salvar nota:", r.json().get("error", r.text))
            return False

    except Exception as e:
        print("❌ Erro ao conectar à API:", e)
        return False        
    
def ver_notas_aluno(usuario_id):    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("📊 Minhas Notas")
    print("="*40)

    try:
        r = requests.get(f"{API_URL}/notas/aluno/{usuario_id}")

        # Tenta converter em JSON, mas trata se não for possível
        try:
            notas = r.json()
        except ValueError:
            print("\n❌ Resposta inválida da API:", r.text)
            input("\nPressione Enter para voltar...")
            return

        if r.status_code != 200:
            print("\n❌ Erro ao buscar notas:", notas.get("error", r.text))
        elif not notas:
            print("\n⚠️ Nenhuma nota encontrada.")
        else:
            for nota in notas:
                print(f"Atividade: {nota['atividade_nome']} | Nota: {nota['nota']}")

    except requests.exceptions.RequestException as e:
        print("\n❌ Erro ao conectar à API:", e)

    input("\nPressione Enter para voltar...")


   