import requests
import time
from front_end.cla_menu import menu_principal

API_URL = "http://127.0.0.1:5000"

def login_usuario():
    try:
        print("\n====== Login ======")
        email = input("Email: ")
        senha = input("Senha: ")

        r = requests.post(f"{API_URL}/usuario/signin", json={"email": email, "senha": senha})
        if r.status_code != 200:
            print("❌ Falha no login:", r.json().get("message", "Erro desconhecido"))
            return None

        usuario = r.json().get("usuario")
        if not usuario:
            print("❌ Dados do usuário não recebidos")
            return None

        # ⚠️ Verifica se é senha temporária
        if usuario.get("senha_temporaria"):
            print("\n⚠️ Essa é uma senha temporária. Você precisa alterá-la antes de continuar.")
            nova_senha = input("Digite a nova senha: ")
            confirmar = input("Confirme a nova senha: ")

            if nova_senha != confirmar:
                print("❌ As senhas não coincidem. Tente novamente.")
                return None

            # Envia requisição para atualizar senha
            alterar = requests.put(
                f"{API_URL}/usuario/alterar_senha",
                json={"email": email, "nova_senha": nova_senha}
            )

            if alterar.status_code == 200:
                print("✅ Senha atualizada com sucesso! Faça login novamente.\n")
                return None
            else:
                print("❌ Erro ao alterar senha:", alterar.json().get("message", "Erro desconhecido"))
                return None

        # Se não for senha temporária, prossegue normalmente
        print(f"✅ Login bem-sucedido! Bem-vindo, {usuario.get('nome', 'Usuário')}!")
        time.sleep(1)
        menu_principal(usuario)

        return usuario

    except requests.exceptions.RequestException as e:
        print("❌ Erro de conexão com a API:", e)
        return None
    except Exception as e:
        print("❌ Erro inesperado:", e)
        return None
