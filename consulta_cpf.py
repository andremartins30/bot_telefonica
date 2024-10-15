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

def consulta_cpf(cpf):
    try:
        print(f"Iniciando consulta para CPF: {cpf}")

        driver.get('https://valentinatelefonica.my.site.com/s/busca-por-linha')
        combobox = wait_and_find_element(driver, By.XPATH, "//input[contains(@class, 'slds-input') and @role='combobox']", timeout=5)
        
        if not combobox:
            combobox = wait_and_find_element(driver, By.ID, "comboboxId-41", timeout=5)
        ActionChains(driver).move_to_element(combobox).click().perform()

        cpf_option = wait_and_find_element(driver, By.XPATH, "//div[@role='option' and contains(., 'CPF')]", timeout=5)
        if cpf_option:
            ActionChains(driver).move_to_element(cpf_option).click().perform()

        input_cpf = wait_and_find_element(driver, By.XPATH, "//*[@id='input2-54']", timeout=5)
        input_cpf.clear()
        
        actions = ActionChains(driver)
        actions.move_to_element(input_cpf).click().send_keys(cpf).perform()

        button_buscar = wait_and_find_element(driver, By.XPATH, '//button[contains(., "Buscar")]', timeout=5)
        driver.execute_script("arguments[0].scrollIntoView(true);", button_buscar)
        actions.move_to_element(button_buscar).click().perform()

        # Espera curta para verificar a presença do elemento que indica que o cliente não existe
        time.sleep(2)
        
        try:
            driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/div/c-feu-interaction-launcher-omni-portuguese-brazil/div/article/div[2]/vlocity_cmt-omniscript-step[7]/div[2]/slot/vlocity_cmt-omniscript-custom-lwc[1]/slot/c-cf-val-create-account-btn/div/vlocity_cmt-flex-card-state/div/slot/div/div[1]/vlocity_cmt-output-field/div/lightning-formatted-rich-text/span/div/span')
            raise NoSuchElementException("Nenhum registro encontrado para esse CPF")
        except NoSuchElementException:
            # Se o elemento não for encontrado, continua com a lógica existente
            button_abrir = wait_and_find_element(driver, By.XPATH, '//a[contains(., "Abrir")]')
            if button_abrir:
                driver.execute_script("arguments[0].scrollIntoView(true);", button_abrir)
                actions.move_to_element(button_abrir).click().perform()
            else:
                raise NoSuchElementException("Nenhum registro encontrado para esse CPF")
            
            wait_for_page_load(driver)
            time.sleep(8)

            button_detalhes = wait_and_find_element(driver, By.XPATH, '//a[contains(@class, "slds-action_item") and @aria-label="Detalhes do Cliente"]')
            if button_detalhes:
                actions.move_to_element(button_detalhes).click().perform()
                print("Botão 'Detalhes do Cliente' clicado com sucesso.")
            else:
                raise NoSuchElementException("Elemento 'Detalhes do Cliente' não encontrado")
            
            wait_for_page_load(driver)
            time.sleep(3)  # Ajuste o tempo conforme necessário

    except Exception as e:
        error_message = f"Erro ao realizar consulta para CPF: {cpf}, erro: {str(e)}"
        print(error_message)
        raise

def buscar_informacoes():
    try:

        time.sleep(8)

        wait_for_page_load(driver)

        nome_cliente = wait.until(EC.presence_of_element_located((By.XPATH, '//h1//span//strong'))).text.strip()
        elemento_span_text = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@style, "font-size: 20px;")]'))).text.strip()
        elemento_p = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/c-val-account-details-page-english/div/article/div[2]/vlocity_cmt-omniscript-step/div[2]/slot/vlocity_cmt-omniscript-custom-lwc[1]/slot/c-cf-val-review-customer/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div/vlocity_cmt-block/div/div/div/slot/div/div[1]/vlocity_cmt-block/div/div/div/slot/div/div/vlocity_cmt-block/div/div/div/slot/div/div[1]/vlocity_cmt-output-field/div/lightning-formatted-rich-text/span/div/p')))
        elemento_p_text = elemento_p.text.strip()

        informacoes = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[contains(@class, "field-value")]')))
        resultados = [info.text for info in informacoes]
        
        resultados.insert(1, nome_cliente)
        resultados.insert(2, elemento_span_text)
        resultados.insert(3, elemento_p_text)
        
        positions_to_remove = [10, 13, 14, 15, 16, 19]
        for pos in sorted(positions_to_remove, reverse=True):
            if pos < len(resultados):
                del resultados[pos]

        driver.back()

        time.sleep(5)

        return resultados
    
    except (TimeoutException, NoSuchElementException):
        print("Erro ao buscar informações.")
        return []

def cliente_possui_oferta():
    try:
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

        # Verificar se o elemento oferta4 foi encontrado e clicar nele
        if oferta4:
            oferta4[0].click()
            print('Elemento 4 clicado')
            
            # Localizar os detalhes da oferta 4
            titulo_oferta4 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[5]/article/div[2]/div/div[1]/div[2]/b/lightning-formatted-text')
            p_oferta4 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[5]/article/div[2]/div/div[2]/div/p/b')
            valor_oferta4 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/div[5]/article/div[2]/div/div[3]/strong')
            ofertas.extend([titulo_oferta4.text, p_oferta4.text, valor_oferta4.text])

        # Verificar se o elemento oferta5 foi encontrado e clicar nele
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

def is_cpf_format(text):
    return re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', text) is not None

def format_cpf(cpf):
    if pd.isna(cpf):
        return ""
    return re.sub(r'\D', '', str(cpf))

def buscar_financeiro(cpf):
    try:
        financeiro = wait_and_find_element(driver, By.XPATH, '//span[contains(text(), "Financeiro")]', timeout=10)
        if financeiro:
            financeiro.click()
            print("Financeiro clicado com sucesso.")
        else:
            print("Elemento 'Financeiro' não encontrado.")
            return []

        time.sleep(12)

        wait_for_page_load(driver)

        element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//strong[contains(text(), 'Histórico de Faturas')]"))
        )

        time.sleep(2)

        print("Elemento encontrado: Histórico de Faturas", element)

        historico1 = driver.find_elements(By.XPATH, '//div[contains(@class, "slds-grid slds-wrap slds-border_bottom slds-p-top_x-small slds-m-right_large slds-text-longform") and contains(@style, "border-bottom: 1px solid rgb(204, 204, 204);")]')
        
        historico_financeiro1 = []

        if historico1:
            for elemento in historico1:
                dados = elemento.text.replace('\n', ', ').split(', ')
                dados.insert(0, cpf)
                while len(dados) < 6:  # Preencher colunas vazias com strings vazias
                    dados.append('')
                historico_financeiro1.append(dados)
        else:
            print("Histórico Financeiro não encontrado.")

        return historico_financeiro1

    except Exception as e:
        print(f"Erro ao buscar financeiro: {e}")
        return []
    
def validar_cpfs(cpfs):
    regex = re.compile(r'^\d{11}$')
    cpfs_validos = [cpf for cpf in cpfs if regex.match(cpf)]
    return cpfs_validos

def run_and_save_to_dataframe(cpfs):
    cpfs_validos = validar_cpfs(cpfs)
    
    if not cpfs_validos:
        print("Nenhum CPF válido encontrado.")
        return
    
    colunas_ofertas = ['CPF', 'Nome do Cliente', 'Protocolo', 'Segmento', 'Data de Nascimento', 'Tempo como cliente Movel', 'Tempo como cliente Fixa', 'Telefone Principal', 'Email Principal', 'Tipo de Cliente', 'Nome', 'Sobrenome', 'Telefone Alternativo 1', 'Telefone Alternativo 2', 'Email Alternativo', 'CEP', 'Estado', 'Cidade', 'Bairro', 'Logradouro', 'Numero', 'Complemento', 'Linha do Endereço', 'Oferta', 'Descrição Oferta', 'Valor Oferta', 'Oferta 2', 'Descrição Oferta 2', 'Valor Oferta 2', 'Oferta 3', 'Descrição Oferta 3', 'Valor Oferta 3', 'Oferta 4', 'Descrição Oferta 4', 'Valor Oferta 4', 'Oferta 5', 'Descrição Oferta 5', 'Valor Oferta 5']
    df_ofertas = pd.DataFrame(columns=colunas_ofertas)
    
    colunas_financeiro = ['CPF', 'Mês de Referência', 'Valor Total', 'Status do Pagamento', 'Status da Fatura', 'Data do vencimento']
    df_financeiro = pd.DataFrame(columns=colunas_financeiro)

    try:
        for cpf in tqdm(cpfs_validos, desc="Processando CPFs", unit="CPF"):
            try:
                consulta_cpf(cpf)
                resultados = buscar_informacoes()
                
                if cliente_possui_oferta():
                    ofertas = buscar_ofertas()
                    if ofertas:
                        resultados.extend(ofertas)
                else:
                    resultados.append("Cliente não possui nenhuma oferta")
                while len(resultados) < len(colunas_ofertas):
                    resultados.append('')
                
                if resultados:
                    df_ofertas.loc[len(df_ofertas)] = resultados
                    print(f"Informações do CPF {cpf} armazenadas.")
                else:
                    print(f"Nenhuma informação coletada para o CPF {cpf}.")
                
                historico_financeiro = buscar_financeiro(cpf)
                for linha in historico_financeiro:
                    while len(linha) < len(colunas_financeiro):  # Preencher colunas vazias com strings vazias
                        linha.append('')
                    df_financeiro.loc[len(df_financeiro)] = linha

                # Salvar os DataFrames em arquivos temporários após cada CPF processado
                df_ofertas.to_csv('dados_ofertas_temp.csv', index=False, encoding='utf-8')
                df_financeiro.to_csv('financeiro_temp.csv', index=False)

            except Exception as e:
                print(f"Erro ao processar CPF {cpf}: {str(e)}")
                driver.save_screenshot(f"error_screenshot_{cpf}.png")
                print(f"Screenshot salvo como error_screenshot_{cpf}.png")
                continue

    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        # Salvar os DataFrames em arquivos temporários antes de sair
        df_ofertas.to_csv('dados_ofertas_temp.csv', index=False, encoding='utf-8')
        df_financeiro.to_csv('financeiro_temp.csv', index=False)
        raise

    # Salvar os DataFrames finais em arquivos
    df_ofertas.to_csv('dados_ofertas.csv', index=False, encoding='utf-8')
    print("Dados armazenados no arquivo 'dados_ofertas.csv'.")
    
    df_financeiro.to_csv('financeiro.csv', index=False)
    print("Dados armazenados no arquivo 'financeiro.csv'.")

# Lista de CPFs para consulta
cpfs = [
'95216073272',
'94598312220',
'94477787200',
'91648637191',
'88882594220',
]

# Rodar o script
run_and_save_to_dataframe(cpfs)

print("Processo concluído.") 