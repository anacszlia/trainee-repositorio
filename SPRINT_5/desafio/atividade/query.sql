SELECT
    MIN(CAST(TaxaCompraManha AS DECIMAL(10, 2))) AS min_taxa_compra,
    MAX(CAST(TaxaVendaManha AS DECIMAL(10, 2))) AS max_taxa_venda
FROM s3object 
WHERE
    (UPPER("TipoTitulo") = 'Tesouro Selic' 
    OR TipoTitulo = 'Tesouro IPCA+ com Juros Semestrais')

    OR (CAST(TaxaCompraManha AS DECIMAL(10, 2)) > 0
    AND CAST(TaxaVendaManha AS DECIMAL(10, 2)) > CAST(TaxaCompraManha AS DECIMAL(10, 2)))

    OR NULLIF(DataBase, DataVencimento) IS NOT NULL AND (CAST(COALESCE(DataBase, '01-01-2005') AS STRING) != '01-01-2005' or UTCNOW())


