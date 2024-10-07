import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configurações do Chrome (certifique-se de que o Chrome foi iniciado em modo de depuração)
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
service = Service('C:/Users/User/Desktop/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)
print("Conectado à sessão existente.")

def cliente_possui_oferta():
    try:
        # Tentar localizar o elemento da oferta
        oferta = driver.find_elements(By.XPATH, '//label[contains(@class, "page")]')
        return len(oferta) > 0
    except NoSuchElementException:
        return False

def buscar_ofertas():
    try:
        ofertas = []

        # Localizar os elementos das ofertas pelo XPath
        oferta1 = driver.find_elements(By.XPATH, '//label[@data-selected-index="0" and contains(@class, "page1")]')
        oferta2 = driver.find_elements(By.XPATH, '//label[@data-selected-index="1" and contains(@class, "page2")]')
        oferta3 = driver.find_elements(By.XPATH, '//label[@data-selected-index="2" and contains(@class, "page3")]')
        oferta4 = driver.find_elements(By.XPATH, '//label[@data-selected-index="3" and contains(@class, "page4")]')
        oferta5 = driver.find_elements(By.XPATH, '//label[@data-selected-index="4" and contains(@class, "page5")]')
        
        # Verificar se o elemento oferta1 foi encontrado e clicar nele
        if oferta1:
            oferta1[0].click()
            print("Elemento 1 clicado com sucesso.")
            
            # Localizar os detalhes da oferta 1
            titulo_oferta1 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[2]/article/div[2]/div/div[1]/div[2]/b/lightning-formatted-text')
            p_oferta1 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[2]/article/div[2]/div/div[2]/div/p/b')
            valor_oferta1 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[2]/article/div[2]/div/div[3]/strong')
            ofertas.extend([titulo_oferta1.text, p_oferta1.text, valor_oferta1.text])
        
        # Verificar se o elemento oferta2 foi encontrado e clicar nele
        if oferta2:
            oferta2[0].click()
            print('Elemento 2 clicado')
            
            # Localizar os detalhes da oferta 2
            titulo_oferta2 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[3]/article/div[2]/div/div[1]/div[2]/b/lightning-formatted-text')
            p_oferta2 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[3]/article/div[2]/div/div[2]/div/p/b')
            valor_oferta2 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[3]/article/div[2]/div/div[3]/strong')
            ofertas.extend([titulo_oferta2.text, p_oferta2.text, valor_oferta2.text])

        # Verificar se o elemento oferta3 foi encontrado e clicar nele
        if oferta3:
            oferta3[0].click()
            print('Elemento 3 clicado')
            
            # Localizar os detalhes da oferta 3
            titulo_oferta3 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[4]/article/div[2]/div/div[1]/div[2]/b/lightning-formatted-text')
            p_oferta3 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[4]/article/div[2]/div/div[2]/div/p/b')
            valor_oferta3 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[4]/article/div[2]/div/div[3]/strong')
            ofertas.extend([titulo_oferta3.text, p_oferta3.text, valor_oferta3.text])

        # Verificar se o elemento oferta3 foi encontrado e clicar nele
        if oferta4:
            oferta4[0].click()
            print('Elemento 4 clicado')
            
            # Localizar os detalhes da oferta 3
            titulo_oferta4 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[5]/article/div[2]/div/div[1]/div[2]/b/lightning-formatted-text')
            p_oferta4 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[5]/article/div[2]/div/div[2]/div/p/b')
            valor_oferta4 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[5]/article/div[2]/div/div[3]/strong')
            ofertas.extend([titulo_oferta4.text, p_oferta4.text, valor_oferta4.text])

        # Verificar se o elemento oferta3 foi encontrado e clicar nele
        if oferta5:
            oferta5[0].click()
            print('Elemento 5 clicado')
            
            # Localizar os detalhes da oferta 5
            titulo_oferta5 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[6]/article/div[2]/div/div[1]/div[2]/b/lightning-formatted-text')
            p_oferta5 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[6]/article/div[2]/div/div[2]/div/p/b')
            valor_oferta5 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[6]/article/div[2]/div/div[3]/strong')
            ofertas.extend([titulo_oferta5.text, p_oferta5.text, valor_oferta5.text])

        return ofertas
    
    except Exception as e:
        print(f"Erro ao buscar ofertas: {str(e)}")
        return None

# Exemplo de uso das funções
if cliente_possui_oferta():
    ofertas = buscar_ofertas()
    print("Informações coletadas:", ofertas)
else:
    print("Cliente não possui oferta.")