# psel-shinier-2023

## Subindo o backup do banco de dados no SGBD
Passo a passo seguido:
### Restaurar o backup
1. Primeiro baixar um arquivo de backup de um banco de dados do Firebird (extensão .fbk)
2. Baixar o Firebird versão 4.0
3. Gerar um arquivo restaurado (extensão .fdb): Abrir o Prompt de Comando no local do arquivo *gbak* e colocar o comando:
`gbak -c -v -user <nome_do_usuario> -password <senha_do_usuario> <caminho_para_arquivo.fbk> <caminho_para_nova_base.fdb>`
### Subir no SGBD
1. Baixar um SGBD (Escolhi o DBeaver)
2. Criar uma nova *Database Connection* com o arquivo gerado nos passos anteriores


## Extraindo informações do banco de dados
### Estudando o banco
Primeiro eu procurei por informações necessárias nas tabelas do banco. A tabela final possui as seguintes colunas:
- Nome da clínica
- Nome do paciente
- Descrição do lançamento
- Forma de pagamento
- Valor a pagar
- Valor pago
- Data de criação do lançamento
- Data de vencimento
- Data de confirmação de pagamento
- Data de recebimento

Aqui está um [esboço](esboco_banco_teste.png) que fiz um esboço para entender melhor as tabelas.

### Extraindo Informações 
Depois de entender melhor o banco, fiz alguns scripts em SQL para extrair as informações, até chegar no resultado. Todas as versões desses comandos estão na pasta [queries_SQL](queries_SQL).

## Enviando para a API
Usei o *Visual Studio Code* e instalei o plugin *REST Client*

Existem duas requisições, na primeira, envio um JSON e ela retorna um bearer token e um id para usar na segunda requisição, onde mando o arquivo csv.

## Automatizando o processo
Para automatizar todas as atvidades anteriores, resolvi fazer alguns scripts em Python. 

### Conexão com o banco de dados
Para fazer a conexão utilizei uma biblioteca *fbd* instalada com o seguinte comando:
`pip install fbd`

O script da automatização pode ser encontrado [aqui](python_scripts).
