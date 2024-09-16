import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re

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

        WebDriverWait(driver, 10)

        # Verificar se o primeiro histórico existe
        historico1 = driver.find_elements(By.XPATH, '//*[@id="704:0"]/div/div[2]/c-cf-val-billing-history-container/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div[3]/c-cf-val-billing-history-data/div/vlocity_cmt-flex-card-state[1]/div/slot/div/div[1]/vlocity_cmt-flex-action/div/a/span')
        
        if len(historico1) > 0:
            # Capturar dados do primeiro histórico
            mes1 = driver.find_element(By.XPATH, '//*[@id="704:0"]/div/div[2]/c-cf-val-billing-history-container/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div[3]/c-cf-val-billing-history-data/div/vlocity_cmt-flex-card-state[1]/div/slot/div/div[1]/vlocity_cmt-flex-action/div/a/span')
            valor_total1 = driver.find_element(By.XPATH, '//*[@id="704:0"]/div/div[2]/c-cf-val-billing-history-container/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div[3]/c-cf-val-billing-history-data/div/vlocity_cmt-flex-card-state[1]/div/slot/div/div[2]/vlocity_cmt-output-field/div/div/span')
            status_pagamento1 = driver.find_element(By.XPATH, '//*[@id="704:0"]/div/div[2]/c-cf-val-billing-history-container/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div[3]/c-cf-val-billing-history-data/div/vlocity_cmt-flex-card-state[1]/div/slot/div/div[3]/vlocity_cmt-output-field/div/lightning-formatted-rich-text/span/div/span')
            status_fatura1 = driver.find_element(By.XPATH, '//*[@id="704:0"]/div/div[2]/c-cf-val-billing-history-container/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div[3]/c-cf-val-billing-history-data/div/vlocity_cmt-flex-card-state[1]/div/slot/div/div[4]/vlocity_cmt-output-field/div/lightning-formatted-rich-text/span/div/span')
            data_vencimento1 = driver.find_element(By.XPATH, '//*[@id="704:0"]/div/div[2]/c-cf-val-billing-history-container/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div[3]/c-cf-val-billing-history-data/div/vlocity_cmt-flex-card-state[1]/div/slot/div/div[5]/vlocity_cmt-output-field/div/div/span')

            print('Historico Financeiro 1:', [cpf, mes1.text, valor_total1.text, status_pagamento1.text, status_fatura1.text, data_vencimento1.text])
        
        else:
            print("Histórico 1 não encontrado.")

        # Verificar se o segundo histórico existe
        historico2 = driver.find_elements(By.XPATH, '//*[@id="704:0"]/div/div[2]/c-cf-val-billing-history-container/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div[3]/c-cf-val-billing-history-data/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-flex-action/div/a/span/span')
        
        if len(historico2) > 0:
            # Capturar dados do segundo histórico
            mes2 = driver.find_element(By.XPATH, '//*[@id="704:0"]/div/div[2]/c-cf-val-billing-history-container/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div[3]/c-cf-val-billing-history-data/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-flex-action/div/a/span/span')
            valor_total2 = driver.find_element(By.XPATH, '//*[@id="704:0"]/div/div[2]/c-cf-val-billing-history-container/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div[3]/c-cf-val-billing-history-data/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[2]/vlocity_cmt-output-field/div/div/span')
            status_pagamento2 = driver.find_element(By.XPATH, '//*[@id="704:0"]/div/div[2]/c-cf-val-billing-history-container/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div[3]/c-cf-val-billing-history-data/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[3]/vlocity_cmt-output-field/div/lightning-formatted-rich-text/span/div/span')
            status_fatura2 = driver.find_element(By.XPATH, '//*[@id="704:0"]/div/div[2]/c-cf-val-billing-history-container/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div[3]/c-cf-val-billing-history-data/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[4]/vlocity_cmt-output-field/div/lightning-formatted-rich-text/span/div/span')
            data_vencimento2 = driver.find_element(By.XPATH, '//*[@id="704:0"]/div/div[2]/c-cf-val-billing-history-container/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div[3]/c-cf-val-billing-history-data/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[5]/vlocity_cmt-output-field/div/div/span')

            print('Historico Financeiro 2:', [cpf, mes2.text, valor_total2.text, status_pagamento2.text, status_fatura2.text, data_vencimento2.text])
        
        else:
            print("Histórico 2 não encontrado.")


        historico3 = driver.find_elements(By.XPATH, '//*[@id="704:0"]/div/div[2]/c-cf-val-billing-history-container/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div[3]/c-cf-val-billing-history-data/div/vlocity_cmt-flex-card-state[4]/div/slot/div')

        historico_financeiro3 = []

        if historico3:
            # Capturar dados do terceiro histórico
            for elemento in historico3:
                # Remover os caracteres de nova linha e separar cada item
                dados = elemento.text.replace('\n', ', ').split(', ')
                dados.insert(0, cpf)
                historico_financeiro3.extend(dados)
            print('Historico Financeiro 3:', historico_financeiro3)
        else:
            print("Histórico 3 não encontrado.")

    except NoSuchElementException:
        print("Elemento financeiro não encontrado.")

buscar_financeiro()