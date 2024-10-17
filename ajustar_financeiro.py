import pandas as pd
import csv

def verificar_colunas(linha):
    """
    Verifica se uma linha tem todas as 6 colunas preenchidas corretamente.
    Retorna True se precisar de ajuste, False caso contrário.
    """
    return len(linha) != 6 or pd.isna(linha[3]) or linha[3] == ''

def ajustar_linha(linha):
    """
    Ajusta uma linha que não está com as 6 colunas corretas.
    Reorganiza os dados e adiciona 'Não informado' onde necessário.
    """
    # Se a linha tiver menos que 6 colunas ou a coluna 4 (índice 3) estiver vazia
    if len(linha) < 6:
        # Criar uma nova lista com 6 elementos
        nova_linha = []
        # Copiar os primeiros 3 elementos
        for i in range(min(3, len(linha))):
            nova_linha.append(linha[i])
        
        # Adicionar "Não informado"
        nova_linha.append("Não informado")
        
        # Adicionar os elementos restantes
        for i in range(3, len(linha)):
            nova_linha.append(linha[i])
        
        # Completar com valores vazios se necessário
        while len(nova_linha) < 6:
            nova_linha.append("")
            
        return nova_linha
    else:
        # Se a coluna 4 (índice 3) estiver vazia
        linha[3] = "Não informado"
        return linha

def ajustar_financeiro(file_path):
    """
    Função principal que processa o arquivo CSV.
    """
    try:
        # Ler o arquivo CSV original
        linhas_originais = []
        with open(file_path, 'r', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            linhas_originais = list(leitor)

        # Processar cada linha
        linhas_ajustadas = []
        for linha in linhas_originais:
            if verificar_colunas(linha):
                linha_ajustada = ajustar_linha(linha)
            else:
                linha_ajustada = linha
            linhas_ajustadas.append(linha_ajustada)

        # Salvar o arquivo ajustado
        nome_arquivo_ajustado = file_path.replace('.csv', '.csv')
        with open(nome_arquivo_ajustado, 'w', encoding='utf-8', newline='') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerows(linhas_ajustadas)

        print(f"Arquivo processado com sucesso. Salvo como: {nome_arquivo_ajustado}")
        
        # Exibir estatísticas do processamento
        total_linhas = len(linhas_originais)
        linhas_ajustadas_count = sum(1 for i in range(len(linhas_originais)) 
                                if linhas_ajustadas[i] != linhas_originais[i])
        
        print(f"\nEstatísticas do processamento:")
        print(f"Total de linhas processadas: {total_linhas}")
        print(f"Linhas que precisaram de ajuste: {linhas_ajustadas_count}")
        
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")

if __name__ == "__main__":
    # Arquivos a serem processados
    arquivos = ['financeiro.csv', 'financeiro_temp.csv']
    
    for arquivo in arquivos:
        print(f"\nProcessando arquivo: {arquivo}")
        ajustar_financeiro(arquivo)