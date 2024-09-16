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

def buscar_informacoes():
    try:
        wait = WebDriverWait(driver, 30)
        time.sleep(15)

        nome_cliente = wait.until(EC.presence_of_element_located((By.XPATH, '//h1//span//strong'))).text.strip()
        elemento_span_text = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@style, "font-size: 20px;")]'))).text.strip()
        elemento_p_text = wait.until(EC.presence_of_element_located((By.XPATH, '(//p)[4]'))).text.strip()

        informacoes = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[contains(@class, "field-value")]')))

        resultados = [info.text for info in informacoes]

        # Tratamento dos dados
        resultados[0] = resultados[0].replace('.', '').replace('-', '')
        resultados.insert(1, nome_cliente)
        resultados.insert(2, elemento_span_text)
        resultados.insert(3, elemento_p_text)
        
        positions_to_remove = [10, 13, 14, 15, 16, 19]
        for pos in sorted(positions_to_remove, reverse=True):
            if pos < len(resultados):
                del resultados[pos]

        driver.back()

        print('Voltando para pagina do cliente')

        return resultados
    
    except (TimeoutException, NoSuchElementException):
        print("Erro ao buscar informações.")
        return []


def buscar_ofertas():
    try:

        oferta1 = driver.find_element(driver, By.XPATH['/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[1]/label[1]'])
        
        if oferta1:
            oferta1.click()    
            titulo_oferta = driver.find_element(driver, By.XPATH['/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[2]/article/div[2]/div/div[1]/div[2]/b/lightning-formatted-text'])
            print('oferta encontrada', titulo_oferta)

    except Exception as e:
        print(f"Erro ao buscar ofertas: {str(e)}")
    
# Exemplo de uso da função
resultados = buscar_informacoes()
ofertas = buscar_ofertas()
print("Informações coletadas:", resultados, ofertas)