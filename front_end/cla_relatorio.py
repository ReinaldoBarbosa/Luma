import requests
import csv
from reportlab.pdfgen import canvas

API_URL = "http://127.0.0.1:5000"

def gerar_relatorio_cli(usuario_id):
    try:
        # Faz a requisição para a API
        r = requests.post(f"{API_URL}/relatorio/gerar", json={"usuario_id": usuario_id})
        if r.status_code != 200:
            print("❌ Erro ao gerar relatório:", r.json().get("error", "Erro desconhecido"))
            return

        relatorio = r.json()["relatorio"]

        # Mostra dados no terminal
        print("\n📊 Relatório Gerado com Sucesso!")
        print(f"🧍 Usuário ID: {relatorio['usuario_id']}")
        print(f"📘 Total de Atividades: {relatorio['total_atividades']}")
        print(f"⭐ Média Geral: {relatorio['media_geral']}")
        print(f"📅 Data: {relatorio['data_geracao']}")

        # Escolher formato
        print("\nDeseja exportar o relatório?")
        print("1️⃣  PDF")
        print("2️⃣  CSV")
        print("3️⃣  Apenas visualizar")
        escolha = input("Opção: ")

        if escolha == "1":
            gerar_pdf_relatorio(relatorio)
        elif escolha == "2":
            gerar_csv_relatorio(relatorio)
        else:
            print("📄 Relatório não exportado.")

    except Exception as e:
        print("❌ Falha na conexão com a API:", e)

def gerar_pdf_relatorio(relatorio):
    nome_arquivo = f"relatorio_usuario_{relatorio['usuario_id']}.pdf"
    c = canvas.Canvas(nome_arquivo)

    c.drawString(100, 750, "===== RELATÓRIO DE DESEMPENHO =====")
    c.drawString(100, 720, f"Usuário ID: {relatorio['usuario_id']}")
    c.drawString(100, 700, f"Total de Atividades: {relatorio['total_atividades']}")
    c.drawString(100, 680, f"Média Geral: {relatorio['media_geral']}")
    c.drawString(100, 660, f"Data de Geração: {relatorio['data_geracao']}")

    c.save()
    print(f"📁 Relatório salvo como PDF: {nome_arquivo}")

def gerar_csv_relatorio(relatorio):
    nome_arquivo = f"relatorio_usuario_{relatorio['usuario_id']}.csv"
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Usuário ID", "Total de Atividades", "Média Geral", "Data de Geração"])
        writer.writerow([
            relatorio["usuario_id"],
            relatorio["total_atividades"],
            relatorio["media_geral"],
            relatorio["data_geracao"]
        ])
    print(f"📁 Relatório salvo como CSV: {nome_arquivo}")    