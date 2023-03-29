SELECT '' AS nome_da_clinica, e.NOME AS nome_do_paciente, 'Documento ' || c.documento AS Descricao_do_lancamento, b.TIPO_DOC AS Forma_de_pagamento , c.valor AS Valor_a_pagar, b.VALOR AS valor_pago, CAST(c.EMISSAO AS date) AS data_criacao_lancamento, CAST (c.VENCTO AS date) AS data_vencimento, b.TRANSMISSAO AS confirmacao_pagamento, CAST(b.BAIXA AS date) AS data_recebimento
FROM EMD101 e JOIN CRD111 c ON e.CGC_CPF = c.CGC_CPF 
LEFT JOIN BXD111 b ON b.DOCUMENTO = c.DOCUMENTO 
UNION ALL 
SELECT '' AS nome_da_clinica, e.NOME AS nome_do_paciente, m.NOME_TIPO  AS Descricao_do_lancamento, m.TIPO_PAGTO AS Forma_de_pagamento, m.VALOR_PARCELA  AS Valor_a_pagar, m.VALOR AS valor_pago, m.EMISSAO AS data_criacao_lancamento, m.VENCTO AS data_vencimento, m.DATA_PAGTO  AS confirmacao_pagamento, m.DATA_PAGTO AS data_recebimento
FROM EMD101 e JOIN MAN111 m ON e.CGC_CPF = m.CNPJ_CPF
ORDER BY 2, 3