import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from tqdm import tqdm

# Configurações do Chrome
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
service = Service('C:/Users/User/Desktop/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)
print("Conectado à sessão existente.")

wait = WebDriverWait(driver, 30)

def wait_for_page_load(driver, timeout=30):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

def wait_and_find_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        print(f"Elemento encontrado: {value}")
        return element
    except TimeoutException:
        print(f"Tempo esgotado ao procurar o elemento: {value}")
        return None

def consulta_plano():
    time.sleep(2)

    try:
        # Espera até que a página esteja completamente carregada
        wait_for_page_load(driver)
        print("Página carregada completamente.")

        # Espera explícita para o elemento "Produtos"
        produtos = wait_and_find_element(driver, By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/ul/li[1]/a/span[2]", timeout=30)
        if produtos:
            produtos.click()
            print("Produto clicado com sucesso.")

            lista = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "slds-button") and contains(@class, "slds-button_icon") and contains(@class, "slds-button_icon-border-filled") and contains(@class, "slds-is-selected")]'))
            )
            
            time.sleep(5)

            if lista:
                lista.click()
                print("Lista de produtos clicada com sucesso.")

                time.sleep(5)

                # Seleciona a tabela de produtos
                tabela = driver.find_elements(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div/section/div/div/c-cf-val-products-view-selector/div/vlocity_cmt-flex-card-state/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div[5]/vlocity_cmt-block/div/div/div/slot/div/div/c-cf-val-product-table-view/div/vlocity_cmt-flex-card-state/div/slot/div/div[3]/c-cf-val-products-data')

                # Se o elemento foi encontrado, captura o texto
                if tabela:
                    tabela_text = tabela[0].text  # Pega o texto do primeiro elemento encontrado

                    # Divide o texto em uma lista de strings
                    tabela_list = tabela_text.split('\n')

                    # Organiza a lista em uma tabela com 9 colunas
                    dados = [tabela_list[i:i + 9] for i in range(0, len(tabela_list), 9)]

                    # Filtra apenas as colunas 0, 1, 2 e 4
                    dados_filtrados = [[linha[0], linha[1], linha[2], linha[4]] for linha in dados]

                    print("Dados capturados com sucesso.", dados_filtrados)

                    return dados_filtrados
                else:
                    print("Elemento não encontrado.")
                    return []

    except Exception as e:
        print(f"Erro ao procurar o elemento 'Produto': {e}")
        return []

dados = consulta_plano()

if dados:
    # Converte os dados para um DataFrame do Pandas
    df = pd.DataFrame(dados, columns=['Coluna 0', 'Coluna 1', 'Coluna 2', 'Coluna 4'])
    
    # Remove linhas que não contêm dados relevantes
    df = df.dropna(how='all')
    
    # Remove colunas que não contêm dados relevantes
    df = df.dropna(axis=1, how='all')
    
    print(df)

print("Processo concluído.")