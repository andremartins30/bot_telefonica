import threading
import tkinter as tk
from tkinter import ttk
import sys
import importlib.util
import tkinter.messagebox as messagebox

# Variáveis globais para armazenar as referências dos widgets
input_cpfs = None
loading_label = None
progress_bar = None
janela = None  # Variável global para a janela
logs = None  # Variável global para o campo de logs

def autenticar_pagina():
    spec = importlib.util.spec_from_file_location("abrir_e_autenticar", "abrir_e_autenticar.py")
    abrir_e_autenticar = importlib.util.module_from_spec(spec)
    sys.modules["abrir_e_autenticar"] = abrir_e_autenticar
    spec.loader.exec_module(abrir_e_autenticar)

def executar_bot():
    global input_cpfs, loading_label, progress_bar, janela, logs  # Declarar as variáveis como global para poder acessá-las
    
    spec = importlib.util.spec_from_file_location("consulta_cpf", "consulta_cpf.py")
    consulta_cpf = importlib.util.module_from_spec(spec)
    sys.modules["consulta_cpf"] = consulta_cpf
    spec.loader.exec_module(consulta_cpf)
    
    # Ler o conteúdo da caixa de texto e remover espaços em branco e novas linhas
    cpfs_text = input_cpfs.get("1.0", tk.END).strip().replace(" ", "").replace("\n", "")
    
    # Verificar se o comprimento total do texto é múltiplo de 11
    if len(cpfs_text) % 11 != 0:
        raise ValueError("O texto inserido não é um múltiplo de 11 caracteres. Verifique os CPFs inseridos.")
    
    # Dividir o texto em blocos de 11 caracteres
    cpfs = [cpfs_text[i:i+11] for i in range(0, len(cpfs_text), 11)]
    
    # Filtrar blocos que não sejam exatamente 11 caracteres (caso haja algum erro de entrada)
    cpfs = [cpf for cpf in cpfs if len(cpf) == 11]
    
    # Verificar se a lista de CPFs não está vazia
    if not cpfs:
        raise ValueError("Nenhum CPF válido encontrado.")
    
    # Mostrar o indicador de carregamento
    loading_label.config(text="Carregando...")
    
    # Função para executar o bot em um thread separado
    def run_bot():
        try:
            log_message(f"Iniciando consulta para {len(cpfs)} CPFs")
            consulta_cpf.run_and_save_to_dataframe(cpfs)  # Passar a lista completa de CPFs
            log_message("Consulta concluída para todos os CPFs.")
            messagebox.showinfo("Sucesso", "Processo concluído com sucesso!")
        except Exception as e:
            log_error(f"Erro durante a execução: {e}")
            messagebox.showerror("Erro", str(e))
        finally:
            # Esconder o indicador de carregamento
            loading_label.config(text="")
            progress_bar['value'] = 0  # Resetar a barra de progresso
    
    # Iniciar o thread
    threading.Thread(target=run_bot).start()

def log_message(message):
    logs.config(state=tk.NORMAL)
    logs.insert(tk.END, message + "\n")
    logs.config(state=tk.DISABLED)
    logs.yview(tk.END)  # Rolagem automática para o final
    janela.update_idletasks()  # Atualizar a interface gráfica

def log_error(message):
    logs.config(state=tk.NORMAL)
    logs.insert(tk.END, "Erro: " + message + "\n")
    logs.config(state=tk.DISABLED)
    logs.yview(tk.END)  # Rolagem automática para o final
    janela.update_idletasks()  # Atualizar a interface gráfica

# Função para iniciar a janela
def iniciar_janela():
    global input_cpfs, loading_label, progress_bar, janela, logs  # Declarar as variáveis como global para poder modificá-las
    
    # Criação da janela
    janela = tk.Tk()
    janela.title("Bot Valentina SFA")
    
    # Definindo o tamanho da janela
    janela.geometry("500x550")
    
    # Criando uma área de input (caixa de texto)
    label_cpf = tk.Label(janela, text="Inserir CPFs, insira os cpfs separados por vírgula")
    label_cpf.pack(pady=10)
    input_cpfs = tk.Text(janela, height=10, width=50)
    input_cpfs.pack(pady=10)
    
    # Logs (texto fixo)
    label_logs = tk.Label(janela, text="Logs")
    label_logs.pack(pady=5)
    
    # Campo de logs
    logs = tk.Text(janela, height=5, width=50, state=tk.DISABLED)
    logs.pack(pady=10)

    # Indicador de carregamento
    loading_label = tk.Label(janela, text="", fg="red")
    loading_label.pack(pady=5)

    # Barra de progresso
    progress_bar = ttk.Progressbar(janela, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

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