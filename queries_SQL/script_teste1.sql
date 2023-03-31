SELECT '' AS nome_da_clinica, e.NOME AS nome_do_paciente, c.documento AS Descricao_do_lancamento, c.valor AS Valor_a_pagar, b.VALOR AS valor_pago, c.EMISSAO AS data_criacao_lancamento, c.VENCTO AS data_vencimento, b.TRANSMISSAO AS confirmacao_pagamento, b.BAIXA AS data_recebimento, c.SITUACAO 
FROM EMD101 e JOIN CRD111 c ON e.CGC_CPF = c.CGC_CPF 
LEFT JOIN BXD111 b ON b.DOCUMENTO = c.DOCUMENTO 
WHERE e.CLIENTE = 'S'
ORDER BY e.NOME 

--script teste para entender as tabelas, sem a tabela MAN111