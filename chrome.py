import subprocess
import os

# Caminho para o Chrome
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

# Diretório para o perfil do Chrome
user_data_dir = "C:/path/to/chrome-profile"

# Comando para iniciar o Chrome com depuração remota
command = [chrome_path, f"--remote-debugging-port=9222", f"--user-data-dir={user_data_dir}"]

# Iniciar o Chrome
subprocess.Popen(command)