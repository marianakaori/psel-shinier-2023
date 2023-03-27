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
