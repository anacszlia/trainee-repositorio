Desafio 1
```sql

Table "tb_carro" {
  "idCarro" INT
  "classiCarro" TEXT
  "marcaCarro" TEXT
  "modeloCarro" TEXT
  "anoCarro" INT
  "idcombustivel" INT
  "tipoCombustivel" TEXT
}

Table "tb_cliente" {
  "idCliente" INT
  "nomeCliente" TEXT
  "cidadeCliente" TEXT
  "estadoCliente" TEXT
  "paisCliente" TEXT
}

Table "tb_local" {
  "idLocacao" INT
  "dataLocacao" NUM
  "horaLocacao" NUM
  "qtdDiaria" INT
  "vlrDiaria" NUM
  "dataEntrega" NUM
  "horaEntrega" NUM
}

Table "tb_vendas" {
  "idLocacao" int [pk]
  "idCliente" int
  "idCarro" int
  "qtdDiaria" int
  "vlrDiaria" decimal(18,2)
  "idVendedor" int
}

Table "tb_vendedor" {
  "idVendedor" INT
  "nomeVendedor" TEXT
  "sexoVendedor" INT
  "estadoVendedor" TEXT
}
```
![modeloER](/modelos/modelo relacional diagrama.png)

Desafio 2
```sql
CREATE VIEW dim_datas AS
    SELECT dataLocacao,
           dataEntrega
      FROM tb_local;

CREATE VIEW enderecos AS
    SELECT cidadeCliente,
           estadoCliente,
           paisCliente
      FROM tb_cliente
    UNION
    SELECT estadoVendedor
      FROM tb_vendedor;


-- Visualizar: fatos
CREATE VIEW fatos AS
    SELECT qtdDiaria,
           vlrDiaria,
           idLocacao,
           idCliente,
           idCarro,
           idVendedor
      FROM tb_vendas
    UNION
    SELECT sexoVendedor
      FROM tb_Vendedor
    UNION
    SELECT idCombustivel
      FROM tb_carros;

```
![modeloER](./)