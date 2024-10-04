import subprocess
import tkinter as tk
import sys


# Verificar se o selenium está instalado
try:
    import selenium
except ImportError:
    print("O módulo 'selenium' não está instalado. Certifique-se de que o ambiente virtual está ativado e o selenium está instalado.")
    sys.exit(1)

def autenticar_pagina():
    import sys
    import importlib.util
    
    spec = importlib.util.spec_from_file_location("abrir_e_autenticar", "abrir_e_autenticar.py")
    abrir_e_autenticar = importlib.util.module_from_spec(spec)
    sys.modules["abrir_e_autenticar"] = abrir_e_autenticar
    spec.loader.exec_module(abrir_e_autenticar)

def executar_bot():
    import sys
    import importlib.util
    
    spec = importlib.util.spec_from_file_location("consulta_cpf", "consulta_cpf.py")
    consulta_cpf = importlib.util.module_from_spec(spec)
    sys.modules["consulta_cpf"] = consulta_cpf
    spec.loader.exec_module(consulta_cpf)

# Função para iniciar a janela
def iniciar_janela():
    # Criação da janela
    janela = tk.Tk()
    janela.title("Bot Valentina SFA")
    
    # Definindo o tamanho da janela
    janela.geometry("500x400")
    
    # Criando uma área de input (caixa de texto)
    label_cpf = tk.Label(janela, text="Inserir CPFs, insira os cpfs separados por vírgula")
    label_cpf.pack(pady=10)
    input_cpfs = tk.Text(janela, height=10, width=50)
    input_cpfs.pack(pady=10)
    
    # Logs (texto fixo)
    label_logs = tk.Label(janela, text="Logs")
    label_logs.pack(pady=5)
    
    # Botão para autenticar página
    btn_autenticar = tk.Button(janela, text="Autenticar Página", width=20, command=autenticar_pagina)
    btn_autenticar.pack(side=tk.LEFT, padx=50, pady=10)
    
    # Botão para executar bot
    btn_executar = tk.Button(janela, text="Executar Bot", width=20, command=executar_bot)
    btn_executar.pack(side=tk.RIGHT, padx=50, pady=10)
    
    # Iniciar a janela principal
    janela.mainloop()

# Chamando a função para rodar a aplicação
iniciar_janela()