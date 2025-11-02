import requests

API_URL = "http://127.0.0.1:5000/chatbot/chat"

def iniciar_chatbot():
    print("🤖 Luma - Assistente Educacional Inteligente")
    print("Digite 'sair' para encerrar o chat.\n")

    while True:
        user_input = input("Você: ")
        if user_input.lower() == "sair":
            print("Luma: Até mais! 👋")
            break

        try:
            resposta = requests.post(API_URL, json={"mensagem": user_input})
            if resposta.status_code == 200:
                conteudo = resposta.json().get("resposta", "")
                print(f"Luma: {conteudo}\n")
            else:
                print(f"⚠️ Erro ({resposta.status_code}): {resposta.text}")
        except Exception as e:
            print("❌ Erro ao conectar à API:", e)
            break


if __name__ == "__main__":
    iniciar_chatbot()
