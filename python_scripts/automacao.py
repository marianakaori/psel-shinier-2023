import os
import json
from fdb import services, connect
import csv
import requests


def realizarLoginNaAPI():

    with open('secrets.json') as arquivo_de_secrets:
        secrets = json.load(arquivo_de_secrets)

    email_api = secrets['email_api']
    senha_api = secrets['senha_api']

    arquivo_de_secrets.close()

    # Fazer requisição de login
    url = 'https://psel.apoena.shinier.com.br/api/login'
    data = {
        "email": email_api,
        "group_key": "Client",
        "password": senha_api
    }
    response = requests.post(url, data=data)

    # Se o login estiver ok, fazer requisição de envio de arquivo
    if response.ok:
        data = response.json()
    else:
        print(f"Erro na requisição do login. Status code: {response.status_code}")
    
    response.close()

    return data


def realizarEnvioArquivoCSVParaAPI(data):
    token = "Bearer " + data['token']
    user_id = data['user']['id']

    url = "https://psel.apoena.shinier.com.br/api/import/create"
    headers = {
        "Authorization": token,
    }
    body = {
        "type": "psel-shinier-2023",
        "erp": "Psel",
        "user_id": user_id,
    }

    files = {
        'file': ('financeiro.csv', open('financeiro.csv', 'rb'), 'application/excel')
    }

    # Fazer a requisição POST
    response = requests.post(url, headers=headers, data=body, files=files)
    # Verificar a resposta
    if response.ok:
        print("Arquivo enviado com sucesso!")
        response.close()
    else:
        print(f"Erro na requisição. Status code: {response.status_code}")


def main():

    # Recuperar dados sigilosos armazenados em um arquivo .json
    with open('secrets.json') as arquivo_de_secrets:
        secrets = json.load(arquivo_de_secrets)
        
    senha_firebird = secrets['senha_firebird']

    arquivo_de_secrets.close()

    caminho_pasta_bancos_de_dados = "bancos_de_dados"
    nome_arquivo_fbk = 'BancoTeste.fbk'
    nome_arquivo_fdb = 'BancoTeste.fdb'


    # Verificar se o arquivo já existe na pasta
    caminho_absoluto_arquivo_fdb = os.path.abspath(caminho_pasta_bancos_de_dados + os.sep + nome_arquivo_fdb)
    caminho_absoluto_arquivo_fbk = os.path.abspath(caminho_pasta_bancos_de_dados + os.sep + nome_arquivo_fbk)


    if os.path.exists(caminho_absoluto_arquivo_fdb):
        os.remove(caminho_absoluto_arquivo_fdb)  # apagar o arquivo caso ele já exista

    # Restaurar o backup do banco de dados
    con = services.connect(host='localhost', user='sysdba', password=senha_firebird)
    con.restore(caminho_absoluto_arquivo_fbk, caminho_absoluto_arquivo_fdb)
    restore_report = con.readlines()

    str_query = """SELECT '' AS nome_da_clinica, e.NOME AS nome_do_paciente, 'Documento ' || c.documento AS Descricao_do_lancamento, b.TIPO_DOC AS Forma_de_pagamento, CAST(c.VALOR AS decimal(11, 2)) AS Valor_a_pagar, CAST(b.VALOR AS decimal(11, 2)) AS valor_pago, CAST(c.EMISSAO AS date) AS data_criacao_lancamento, CAST (c.VENCTO AS date) AS data_vencimento, b.TRANSMISSAO AS confirmacao_pagamento, CAST(b.BAIXA AS date) AS data_recebimento
    FROM EMD101 e JOIN CRD111 c ON e.CGC_CPF = c.CGC_CPF 
    LEFT JOIN BXD111 b ON b.DOCUMENTO = c.DOCUMENTO 
    UNION ALL 
    SELECT '' AS nome_da_clinica, e.NOME AS nome_do_paciente, m.NOME_TIPO  AS Descricao_do_lancamento, m.TIPO_PAGTO AS Forma_de_pagamento, CAST(m.VALOR_PARCELA AS decimal(11, 2)) AS Valor_a_pagar, CAST(m.VALOR  AS decimal(11, 2)) AS valor_pago, m.EMISSAO AS data_criacao_lancamento, m.VENCTO AS data_vencimento, m.DATA_PAGTO  AS confirmacao_pagamento, m.DATA_PAGTO AS data_recebimento
    FROM EMD101 e JOIN MAN111 m ON e.CGC_CPF = m.CNPJ_CPF
    ORDER BY 2, 3
    FETCH FIRST 20000 ROWS ONLY;"""

    # Conectar ao banco de dados
    conn = connect(dsn = caminho_pasta_bancos_de_dados + os.sep + nome_arquivo_fdb, user = "SYSDBA", password = senha_firebird)


    # Criar um cursor que será responsável por executar a query no banco de dados.
    cursor=conn.cursor()
    cursor.execute(str_query)

    # Criar um arquivo CSV e escrever o resultado da consulta nele
    with open('financeiro.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow([i[0] for i in cursor.description]) # Escreve o cabeçalho
        csvwriter.writerows(cursor.fetchall()) # método fetchall que recupera todas as linhas da consulta retornada

    # Fechar as conexões
    cursor.close()
    conn.close()


    dadosRespostaAPI = realizarLoginNaAPI();

    realizarEnvioArquivoCSVParaAPI(dadosRespostaAPI);

if __name__ == "__main__":
    main()
    