import os
import json
import fdb
from fdb import services
import csv
import requests

with open('secrets.json') as f:
    secrets = json.load(f)

senha_firebird = secrets['senha_firebird']

caminho_pasta_bancos_de_dados = "bancos_de_dados"
nome_arquivo_fbk = 'BancoTeste.fbk'
nome_arquivo_fdb = 'BancoTeste.fdb'


# verificar se o arquivo já existe na pasta
caminho_absoluto_arquivo_fdb = os.path.abspath(caminho_pasta_bancos_de_dados + os.sep + nome_arquivo_fdb)
caminho_absoluto_arquivo_fbk = os.path.abspath(caminho_pasta_bancos_de_dados + os.sep + nome_arquivo_fbk)


if os.path.exists(caminho_absoluto_arquivo_fdb):
    os.remove(caminho_absoluto_arquivo_fdb)  # apagar o arquivo

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

# Conectando ao banco de dados
# Pegando o arquivo de banco já restaurado.
conn = fdb.connect(dsn = caminho_pasta_bancos_de_dados + os.sep + nome_arquivo_fdb, user = "SYSDBA", password = senha_firebird)


# Criando um cursor
cursor=conn.cursor()
cursor.execute(str_query)

# Criando um arquivo CSV e escrevendo os dados da consulta nele
with open('output.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow([i[0] for i in cursor.description]) # Escreve o cabeçalho
    csvwriter.writerows(cursor.fetchall())

# Fechando a conexão
cursor.close()
conn.close()

with open('secrets.json') as f:
    secrets = json.load(f)

email_api = secrets['email_api']
senha_api = secrets['senha_api']

# Fazer requisição de login
url = 'https://psel.apoena.shinier.com.br/api/login'
data = {
    "email": email_api,
    "group_key": "Client",
    "password": senha_api
}
response = requests.post(url, data=data)

# Se login ok, fazer requisição de envio de arquivo
if response.ok:
    data = response.json()

    token = "Bearer " + data['token'] 
    user_id = data['user']['id']
    
    url = "https://psel.apoena.shinier.com.br/api/import/create"
    headers = {
        "Authorization": token,
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    }
    data = {
        "type": "psel-shinier-2023",
        "erp": "Psel",
        "user_id": user_id,
    }

    # Montar o corpo da requisição com o arquivo
    body = (
        "------WebKitFormBoundary7MA4YWxkTrZu0gW\n"
        'Content-Disposition: form-data; name="file"; filename="financeiro.csv"\n'
        "Content-Type: application/excel\n\n"
        "< output.csv\n"
        "------WebKitFormBoundary7MA4YWxkTrZu0gW\n"
    )

    # Adicionar o corpo ao restante dos dados
    body += "------WebKitFormBoundary7MA4YWxkTrZu0gW\n".join(
        f'Content-Disposition: form-data; name="{key}"\n\n{value}\n'
        for key, value in data.items()
    ) + "------WebKitFormBoundary7MA4YWxkTrZu0gW\n"

    # Fazer a requisição POST
    response = requests.post(url, headers=headers, data=body)
    # Verificar a resposta
    if response.ok:
        print("Arquivo enviado com sucesso!")
    else:
        print(f"Erro na requisição. Status code: {response.status_code}")

else:
    print(f"Erro na requisição do login. Status code: {response.status_code}")

