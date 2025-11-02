from api import create_app
from api.database import init_db

app = create_app()

if __name__ == "__main__":
    # Inicializa o banco e cria admin se necessário
    init_db()

    # Roda o servidor Flask
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,          # False em produção
        use_reloader=False    # evita criar duas instâncias no Windows
    )
