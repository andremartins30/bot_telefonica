import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurações do Chrome (certifique-se de que o Chrome foi iniciado em modo de depuração)
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
service = Service('C:/Users/User/Desktop/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)
print("Conectado à sessão existente.")

def is_cpf_format(text):
    return re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', text) is not None

def buscar_financeiro():
    try:

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(@style, "text-decoration:teste;")]'))
        )

        if is_cpf_format(element.text):
            cpf = element.text
            print(f"CPF encontrado: {cpf}")
        else:
            print("CPF não encontrado ou formato inválido")

        financeiro = driver.find_element(By.XPATH, '//span[contains(text(), "Financeiro")]')
        financeiro.click()
        print("Financeiro clicado com sucesso.")

        time.sleep(25)

        # Verificar se o primeiro histórico existe
        historico1 = driver.find_elements(By.XPATH, '//div[contains(@class, "slds-grid slds-wrap slds-border_bottom slds-p-top_x-small slds-m-right_large slds-text-longform") and contains(@style, "border-bottom: 1px solid rgb(204, 204, 204);")]')
        
        historico_financeiro1 = []

        if historico1:
            # Capturar dados do primeiro histórico
            for elemento in historico1:
                # Remover os caracteres de nova linha e separar cada item
                dados = elemento.text.replace('\n', ', ').split(', ')
                dados.insert(0, cpf)
                historico_financeiro1.extend(dados)
            print('Historico Financeiro:', historico_financeiro1)
        else:
            print("Histórico 1 não encontrado.")

        # Exportar para CSV usando pandas
        historico_formatado = []
        linha_atual = []

        for item in historico_financeiro1:
            if re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', item) and linha_atual:
                historico_formatado.append(linha_atual)
                linha_atual = []
            linha_atual.append(item)

        if linha_atual:
            historico_formatado.append(linha_atual)

        # Criar um DataFrame do pandas
        df = pd.DataFrame(historico_formatado, columns=['CPF', 'Mês de Referência', 'Valor Total', 'Status do Pagamento', 'Status da Fatura', 'Data do vencimento'])

        # Exportar para CSV
        df.to_csv('financeiro.csv', index=False)

        print("Dados exportados para 'financeiro.csv' com sucesso.")

    except Exception as e:
        print(f"Erro ao buscar financeiro: {e}")

buscar_financeiro()