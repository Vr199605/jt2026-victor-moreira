# Etapa 1 — Limpeza, Cruzamento e Agregação de Dados | Itapema (SC)

**Seazone | Desafio Jovens Talentos AI Builder 2026**

## 1. Volume de dados (bruto vs. limpo)

| Base               |   Registros brutos |   Registros após limpeza |
|:-------------------|-------------------:|-------------------------:|
| Details (listings) |               4441 |                     4441 |
| Hosts              |               3057 |                     3057 |
| Price_AV (diárias) |             118839 |                   117345 |
| VivaReal (venda)   |               8329 |                     7376 |

## 2. Tratamento de outliers

- **Diárias (Price_AV):** método IQR (k=3, limite mínimo R$30) sobre a base completa. Faixa aceita: R$ 30 – R$ 2018. Removidos 1494 registros (1.3%).
- **Preço de venda e Preço/m² (VivaReal):** método IQR (k=1.5) calculado **por bairro**, para respeitar diferenças de padrão de mercado entre regiões. Área útil restrita a 15–1000 m². Removidos 940 registros (11.3%).

## 3. Normalização de bairros

- **VivaReal:** variações de grafia/caixa (`meia praia`, `MEIA PRAIA`, `Taboleiro`, etc.) foram mapeadas para uma lista canônica de bairros de Itapema.
- **Airbnb (Details):** não há campo de bairro estruturado; o bairro foi **inferido por busca textual** (nome + descrição do anúncio) usando a mesma lista canônica do VivaReal. Bairro não identificado em 49.1% dos anúncios (tratados à parte, não descartados).

## 4. Short Stay — resumo por bairro

ADR mediano (R$/diária), volume mediano de reviews e rating médio, por bairro identificado.

| bairro         |   n_anuncios |   adr_mediano |   reviews_mediano |   rating_medio |   pct_superhost |
|:---------------|-------------:|--------------:|------------------:|---------------:|----------------:|
| Meia Praia     |         1809 |         575   |               2   |            4.8 |             0.2 |
| Centro         |          364 |         592.3 |               3   |            4.8 |             0.2 |
| Morretes       |           37 |         400   |               1   |            4.9 |             0.2 |
| Canto da Praia |           18 |         600   |               5   |            4.9 |             0.2 |
| Ilhota         |           14 |         495   |               8.5 |            4.7 |             0.4 |
| Andorinha      |            7 |         330.8 |              10   |            4.9 |             0.1 |
| Tabuleiro      |            6 |         592   |              10   |            4.9 |             0.3 |
| Casa Branca    |            2 |               |               7.5 |            4.9 |             0   |
| Alto Sao Bento |            1 |         280   |              14   |            4.9 |             0   |
| Estreito       |            1 |               |               2   |            5   |             0   |
| Varzea         |            1 |               |               4   |            3.2 |             1   |

## 5. Venda (VivaReal) — resumo por bairro x nº de quartos

Preço de venda mediano, preço/m² mediano e área útil mediana, por bairro e faixa de quartos (imóveis com 4+ quartos agrupados).

| bairro                  | faixa_quartos   |   n_imoveis |   preco_venda_mediano |   preco_m2_mediano |   area_util_mediana |   condo_mediano |   iptu_mediano |
|:------------------------|:----------------|------------:|----------------------:|-------------------:|--------------------:|----------------:|---------------:|
| Alto São Bento          | 0               |           9 |      560000           |             1250   |               330   |             0   |           50   |
| Alto São Bento          | 2               |          34 |      623035           |             9267   |                67   |             1   |          300   |
| Alto São Bento          | 3               |           5 |      690000           |             7324.8 |                95   |             0   |            0   |
| Alto São Bento          | 4+              |           1 |           1e+06       |             6666.7 |               150   |                 |            0   |
| Andorinha               | 0               |           9 |           2.9e+06     |            16666.7 |               120   |             1   |         1825   |
| Andorinha               | 1               |          12 |      760000           |            17820.7 |                60   |             1   |            0   |
| Andorinha               | 2               |          69 |      950000           |            11187.5 |                84   |           445.5 |          570   |
| Andorinha               | 3               |         415 |           1.6998e+06  |            13743.8 |               122   |           490   |          610   |
| Andorinha               | 4+              |         191 |           2.798e+06   |            15288   |               186   |           650   |          250   |
| Canto da Praia          | 1               |           7 |      780000           |            14220.7 |                50   |           500   |          100   |
| Canto da Praia          | 2               |          11 |           1.21861e+06 |            14080.5 |                87   |             1   |            1   |
| Canto da Praia          | 3               |          72 |           1.9844e+06  |            14850   |               119   |             0   |            0.5 |
| Canto da Praia          | 4+              |          26 |           6.2e+06     |            21642.9 |               280.5 |             1   |            1   |
| Casa Branca             | 0               |          10 |      781000           |             2352.1 |               315.5 |             0   |            0   |
| Casa Branca             | 2               |          21 |      698000           |             9285.7 |                70   |           350   |          100   |
| Casa Branca             | 3               |          24 |           1.54988e+06 |            10662   |               150   |             0   |            0   |
| Casa Branca             | 4+              |          13 |           3.49e+06    |            12830.9 |               272   |            66   |          131   |
| Castelo Branco          | 0               |           5 |           1.88706e+06 |            22465   |                95   |             0.5 |          340   |
| Castelo Branco          | 1               |           2 |           1.5255e+06  |            20436.1 |               166   |             0   |            0   |
| Castelo Branco          | 2               |          52 |           1.055e+06   |            11904.1 |                87.5 |           420   |          597.5 |
| Castelo Branco          | 3               |         268 |           1.6825e+06  |            13590   |               126   |           375.5 |          150   |
| Castelo Branco          | 4+              |         120 |           2.4953e+06  |            14085.4 |               180   |           126.5 |          780   |
| Centro                  | 0               |           3 |           2.145e+06   |            20432.8 |               123   |             1   |          100   |
| Centro                  | 1               |          20 |      895000           |            16401.7 |                49   |           500   |         1000   |
| Centro                  | 2               |          80 |           1.1225e+06  |            13028.9 |                85   |           480   |          682.5 |
| Centro                  | 3               |         399 |           2.1e+06     |            15789.5 |               131   |             1   |            1   |
| Centro                  | 4+              |         406 |           3.9e+06     |            18962.4 |               200   |             0   |            0   |
| Estreito                | 3               |           1 |           2.75e+06    |             9821.4 |               280   |             0   |            0   |
| Estreito                | 4+              |           4 |           5.1075e+06  |            26762.5 |               197.5 |           990   |         1250   |
| Ilhota                  | 0               |           5 |           1.2e+06     |             2000   |               450   |             0   |            0   |
| Ilhota                  | 1               |           5 |      220000           |             5333.1 |                38   |           250   |           60   |
| Ilhota                  | 2               |           1 |      500000           |             6756.8 |                74   |             0   |            0   |
| Ilhota                  | 3               |           5 |           5.04525e+06 |            15697.7 |               362   |             3   |            0   |
| Ilhota                  | 4+              |          31 |           8.9855e+06  |            22651   |               389   |             3   |          100   |
| Jardim Praia Mar        | 0               |           1 |      685000           |             2283.3 |               300   |                 |                |
| Jardim Praia Mar        | 1               |           5 |      740000           |            11935.5 |                62   |             0   |            0.5 |
| Jardim Praia Mar        | 2               |          81 |      729981           |            10879.3 |                64   |           220   |            1   |
| Jardim Praia Mar        | 3               |           8 |      702191           |            10103.2 |                69.5 |           201.5 |          800   |
| Jardim Praia Mar        | 4+              |           1 |           4e+06       |            21052.6 |               190   |             0   |         2850   |
| Meia Praia              | 0               |          27 |           1.9e+06     |            13709.7 |               154   |             0   |            0   |
| Meia Praia              | 1               |          50 |      887500           |            21125   |                40   |           350   |          590   |
| Meia Praia              | 2               |         216 |           1.05e+06    |            12690.5 |                85.5 |           450   |          600   |
| Meia Praia              | 3               |        1531 |           1.88486e+06 |            14912.3 |               129   |           500   |          450   |
| Meia Praia              | 4+              |        1248 |           3.79e+06    |            18617   |               190   |           548.5 |            1   |
| Morretes                | 0               |          80 |      650000           |             2434.4 |               283   |             0   |          500   |
| Morretes                | 1               |          43 |      600000           |            12898.5 |                44   |             0   |           50   |
| Morretes                | 2               |        1133 |      750000           |            11120   |                69   |             1   |          500   |
| Morretes                | 3               |         285 |      790000           |             8333.3 |               100   |             0   |          500   |
| Morretes                | 4+              |          60 |           5.675e+06   |            24965.3 |               188.5 |             1   |         1000   |
| Sertão do Trombudo      | 0               |          11 |      598000           |             1695.3 |               265   |             0   |            0   |
| Sertão do Trombudo      | 1               |           3 |      950000           |            12179.5 |                78   |           510   |            0   |
| Sertão do Trombudo      | 2               |           9 |      680000           |             9315.1 |                90   |             0   |          500   |
| Sertão do Trombudo      | 3               |           2 |           2.065e+06   |            10539.9 |               200   |             0   |            0   |
| Sertão do Trombudo      | 4+              |           3 |           5.2e+06     |            17333.3 |               300   |             0   |         1350   |
| Sertãozinho             | 2               |           1 |      529360           |             9624.7 |                55   |           400   |          800   |
| Tabuleiro dos Oliveiras | 1               |           2 |      699000           |            13066.6 |                53.5 |             0   |            0   |
| Tabuleiro dos Oliveiras | 2               |         105 |      780000           |            11428.6 |                69   |             1   |            1   |
| Tabuleiro dos Oliveiras | 3               |          15 |      885000           |            11285.7 |                70   |           325   |         1000   |
| Tabuleiro dos Oliveiras | 4+              |           2 |           2.54223e+06 |            10599.6 |               273   |             0   |            0   |
| Varzea                  | 0               |           2 |      594500           |             1467.2 |               431.5 |                 |            0   |
| Varzea                  | 2               |          26 |      644900           |             9548.6 |                69   |             0   |            0   |
| Varzea                  | 3               |           5 |      795000           |             9828.6 |                80   |             0   |           17.5 |
| Varzea                  | 4+              |           1 |      899000           |             3825.5 |               235   |             0   |                |

## 6. Observações metodológicas

- ADR = *Average Daily Rate*, calculado como a mediana das diárias observadas no calendário de disponibilidade (Price_AV) por anúncio, e depois agregado por bairro.
- `star_rating` = 0 foi tratado como ausência de avaliação (NaN), não como nota zero.
- Duplicidades de `airbnb_listing_id` e `owner_id` foram removidas mantendo o registro mais recente (`aquisition_date`).
- Apenas imóveis com `business_types == Venda` entraram na agregação de compra e venda (aluguel tradicional foi excluído do escopo desta etapa).
- **Atenção:** células da tabela de bairro x quartos com poucas observações (n < 10) têm baixa robustez estatística e devem ser interpretadas com cautela — há 28 dessas células na tabela completa (disponível em `vivareal_bairro_quartos.csv`).
