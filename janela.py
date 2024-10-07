import subprocess
import tkinter as tk
import sys
import importlib.util
import tkinter.messagebox as messagebox

# Variável global para armazenar a referência da caixa de texto
input_cpfs = None

def autenticar_pagina():
    spec = importlib.util.spec_from_file_location("abrir_e_autenticar", "abrir_e_autenticar.py")
    abrir_e_autenticar = importlib.util.module_from_spec(spec)
    sys.modules["abrir_e_autenticar"] = abrir_e_autenticar
    spec.loader.exec_module(abrir_e_autenticar)

def executar_bot():
    global input_cpfs  # Declarar a variável como global para poder acessá-la
    
    spec = importlib.util.spec_from_file_location("consulta_cpf", "consulta_cpf.py")
    consulta_cpf = importlib.util.module_from_spec(spec)
    sys.modules["consulta_cpf"] = consulta_cpf
    spec.loader.exec_module(consulta_cpf)
    
    # Ler o conteúdo da caixa de texto e dividir os CPFs por vírgula
    cpfs_text = input_cpfs.get("1.0", tk.END).strip()
    cpfs = [cpf.strip() for cpf in cpfs_text.split(",") if cpf.strip()]
    
    # Executar o bot com os CPFs capturados
    consulta_cpf.run_and_save_to_dataframe(cpfs)

# Função para iniciar a janela
def iniciar_janela():
    global input_cpfs  # Declarar a variável como global para poder modificá-la
    
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

    # Campo de logs
    logs = tk.Text(janela, height=10, width=50, state=tk.DISABLED)
    logs.pack(pady=10)

    def log_error(message):
        logs.config(state=tk.NORMAL)
        logs.insert(tk.END, message + "\n")
        logs.config(state=tk.DISABLED)
    
    # Iniciar a janela principal
    janela.mainloop()

# Chamando a função para rodar a aplicação
iniciar_janela()