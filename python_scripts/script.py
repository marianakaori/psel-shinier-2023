import fdb
from fdb import services
import csv
import os
import json

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