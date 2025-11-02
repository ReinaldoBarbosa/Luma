import os, sys

# garante que a raiz do projeto está no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from front_end.cla_login import login_usuario

def iniciar():
    while True:
        print("\n=== LUMA - Sistema Educacional ===")
        print("1️⃣  Login")
        print("0️⃣  Sair")
        opc = input("Escolha: ")

        if opc == "1":
            login_usuario()
        elif opc == "0":
            print("Encerrando o sistema...")
            break

if __name__ == "__main__":
    iniciar()
