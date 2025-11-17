import os
from openai import OpenAI
from dotenv import load_dotenv

# Carregar variáveis de ambiente (.env)
load_dotenv()

# Criar cliente OpenAI (usa sua chave secreta do .env)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def enviar_mensagem(mensagem, historico):
    """
    Recebe uma mensagem do usuário e o histórico da conversa.
    Retorna a resposta gerada pelo modelo.
    """

    # Adiciona a mensagem do usuário ao histórico
    historico.append({"role": "user", "content": mensagem})

    try:
        # Chama o modelo GPT
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",  # leve, rápido e bom para chatbots
            messages=historico,
            temperature=0.8,  # define criatividade
            max_tokens=300
        )

        # Pega o texto gerado
        conteudo = resposta.choices[0].message.content

        # Adiciona a resposta ao histórico
        historico.append({"role": "assistant", "content": conteudo})

        return conteudo

    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")
        return "Desculpe, estou com dificuldades para responder no momento."

