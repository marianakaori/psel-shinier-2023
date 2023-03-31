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
O script da automatização pode ser encontrado [aqui](python_scripts).

### Conexão com o banco de dados

Para fazer a conexão utilizei uma biblioteca *fdb* instalada com o seguinte comando:
`pip install fdb`

### Restauração do banco de dados

A restauração foi feita da seguinte forma:

```sh
con = services.connect(host='localhost', user='sysdba', password=senha_firebird)

con.restore(caminho_absoluto_arquivo_fbk, caminho_absoluto_arquivo_fdb)
restore_report = con.readlines()
```

### Extração de informações

Criei um cursor para executar a query, e então criei um arquivo csv apara escrever os dados do guardados pelo cursor.

### Requisições para a API

As requisições foram feitas usando a biblioteca *requests* instalada com o seguinte comando:
`pip install requests`

## Observações Finais

O processo de automatização foi bem sucedido, porém a API que retorna a diferença entre a planilha enviada e a planilha modelo ainda aponta alguns erros. Acredito que isso acontece por conta de alguma formatação que não consegui encontrar, pois pelo o que observei, todas as linhas enviadas estão retornando. Além disso, a planilha que enviei contém a forma de pagamento em código, e não por extenso.

O recomendado era fazer o script em PHP, mas achei que perderia muito tempo do desafio em si para aprender uma tecnologia nova, por isso escolhi o Python, já que tinha mais familiaridade.

Por fim, deixo meus agradecimentos à empresa Shinier pela experiência, tenho certeza de que aprendi muito nessa semana. Obrigada.
