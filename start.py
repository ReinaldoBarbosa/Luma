import subprocess
import time

print("🚀 Iniciando o servidor Flask (API)...")
api_process = subprocess.Popen(["python", "app.py"])

# Espera o servidor iniciar
time.sleep(2)

print("🖥️ Iniciando o front-end CLI...")
try:
    subprocess.run(["python", "front_end/cla_main.py"])
finally:
    print("🛑 Encerrando o servidor...")
    api_process.terminate()
