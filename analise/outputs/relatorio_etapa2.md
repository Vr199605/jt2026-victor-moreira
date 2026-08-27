# Etapa 2 — Teste de Tese e Drivers de Receita | Itapema (SC)

**Seazone | Desafio Jovens Talentos AI Builder 2026**

## 1. Premissas do modelo

- **Ocupação anual:** 3 cenários — conservador 45%, base 48%, otimista 52% (referência para litoral catarinense).
- **Receita Bruta Anual** = ADR mediano × Ocupação × 365.
- **OPEX estimado ≈ 25%** (taxa de gestão Seazone + condomínio + IPTU, de forma agregada e simplificada).
- **Gross Yield (%)** = Receita Bruta Anual / Preço Mediano de Compra × 100.
- **Net Yield / Cap Rate (%)** = Gross Yield × (1 − 25%).
- **Payback simples (anos)** = Preço Mediano de Compra / Receita Líquida Anual.
- Faixas de quartos: *Compacto* agrupa studio + 1 quarto; demais faixas seguem número de quartos do imóvel.

## 2. Cenários financeiros por bairro x faixa de quartos (cenário BASE — ocupação 48%)

| bairro     | faixa_quartos         |   n_anuncios |   n_imoveis |   adr_mediano |   preco_venda_mediano |   preco_m2_mediano |   area_util_mediana |   condo_mensal_mediano |   iptu_anual_mediano |   receita_bruta_base_48pct |   receita_m2_base_48pct |   gross_yield_base_48pct |   net_yield_base_48pct |   payback_anos_base_48pct |
|:-----------|:----------------------|-------------:|------------:|--------------:|----------------------:|-------------------:|--------------------:|-----------------------:|---------------------:|---------------------------:|------------------------:|-------------------------:|-----------------------:|--------------------------:|
| Centro     | 2 quartos             |          132 |          84 |         520   |           1.1225e+06  |            13009.1 |                86   |                    460 |                  650 |                    91104   |                  1059.3 |                      8.1 |                    6.1 |                      16.4 |
| Centro     | 3+ quartos            |          129 |         801 |         898.5 |           2.7988e+06  |            17105.3 |               156   |                      0 |                    0 |                   157417   |                  1009.1 |                      5.6 |                    4.2 |                      23.7 |
| Centro     | Compacto (0-1 quarto) |          103 |          24 |         427   |      895000           |            20811.7 |                53.5 |                    500 |                  560 |                    74810.4 |                  1398.3 |                      8.4 |                    6.3 |                      15.9 |
| Meia Praia | 2 quartos             |          561 |         219 |         450   |           1.08e+06    |            12766   |                85   |                    450 |                  650 |                    78840   |                   927.5 |                      7.3 |                    5.5 |                      18.3 |
| Meia Praia | 3+ quartos            |         1103 |        2793 |         672.7 |           2.49927e+06 |            16272.7 |               153   |                    500 |                  100 |                   117851   |                   770.3 |                      4.7 |                    3.5 |                      28.3 |
| Meia Praia | Compacto (0-1 quarto) |          145 |          81 |         360   |      980000           |            19000   |                44   |                    250 |                  100 |                    63072   |                  1433.5 |                      6.4 |                    4.8 |                      20.7 |
| Morretes   | 2 quartos             |           24 |        1115 |         400   |      750000           |            11085.7 |                70   |                     10 |                  500 |                    70080   |                  1001.1 |                      9.3 |                    7   |                      14.3 |
| Morretes   | 3+ quartos            |            6 |         337 |               |      840000           |             9217.4 |               105   |                      0 |                  500 |                            |                         |                          |                        |                           |
| Morretes   | Compacto (0-1 quarto) |            7 |         128 |               |      650000           |             7040.6 |               107.5 |                      0 |                  300 |                            |                         |                          |                        |                           |

*(Cenários conservador 45% e otimista 52% completos em `cenarios_financeiros_bairro_quartos.csv`)*

## 3. A tese dos compactos no Centro se confirma?

O segmento **Compacto (0-1 quarto) no Centro** apresenta Net Yield de **6.3%** e payback simples de **15.9 anos** no cenário base.

- **Melhor Net Yield da matriz completa:** Morretes / 2 quartos (7.0%).
- **Melhor payback da matriz completa:** Morretes / 2 quartos (14.3 anos).

**Prós dos compactos no Centro:**
- Ticket de aquisição mais baixo, o que reduz a barreira de entrada de capital por unidade.
- Receita bruta por m² tende a ser mais alta que unidades maiores, pois o ADR não cai na mesma proporção da redução de área.
- Localização central favorece hóspedes a trabalho/curta estadia e reduz dependência de temporada de praia.

**Contras / limitações:**
- Estoque de compactos é uma fatia pequena do mercado (poucos imóveis de 0-1 quarto ofertados no VivaReal em relação a 2 e 3+ quartos), o que limita a escala de aquisições da Seazone nesse segmento.
- Amostra de anúncios de short stay compactos no Centro também é reduzida, tornando o ADR mediano mais sensível a poucos anúncios/outliers.
- ADR absoluto de compactos costuma ser mais baixo que apartamentos de 2-3 quartos em bairros de praia (Meia Praia), o que pode limitar o Gross Yield mesmo com preço de compra menor.

## 4. Drivers de receita — Comodidades

Prêmio de ADR mediano comparando anúncios que declaram a comodidade/atributo vs. os que não declaram (toda a base de Itapema, sem filtro de bairro):

| atributo                         |   n_com |   adr_mediano_com |   n_sem |   adr_mediano_sem |   premio_pct |
|:---------------------------------|--------:|------------------:|--------:|------------------:|-------------:|
| Ar-condicionado                  |     979 |             575   |      12 |               400 |         43.8 |
| Vista mar (declarada no anúncio) |     338 |             650   |     653 |               500 |         30   |
| Churrasqueira                    |     764 |             598.4 |     227 |               485 |         23.4 |
| Vaga de garagem                  |     949 |             575   |      42 |               515 |         11.7 |
| Piscina                          |     135 |             575   |     856 |               575 |          0   |

*Nota: a base de amenidades estruturadas do Airbnb é quase saturada em ar-condicionado (apenas 12 anúncios sem essa comodidade), então esse prêmio específico deve ser lido com cautela estatística; os demais atributos têm amostras mais equilibradas.*

## 5. Drivers de receita — Perfil do anfitrião

| atributo   |   n_superhost |   adr_mediano_superhost |   n_host_comum |   adr_mediano_host_comum |   premio_pct |   reviews_mediano_superhost |   reviews_mediano_host_comum |   rating_medio_superhost |   rating_medio_host_comum |
|:-----------|--------------:|------------------------:|---------------:|-------------------------:|-------------:|----------------------------:|-----------------------------:|-------------------------:|--------------------------:|
| Superhost  |           434 |                     534 |            557 |                    598.8 |        -10.8 |                          26 |                           12 |                      4.9 |                       4.9 |

## 6. Leitura analítica

- **Ar-condicionado** tem o maior prêmio bruto de ADR (+43.8%), mas com amostra de comparação muito pequena (praticamente todos os anúncios já têm ar-condicionado), então o sinal mais confiável vem de **Vista mar (declarada no anúncio)**: prêmio de +30.0% sobre anúncios sem esse atributo, com amostras equilibradas dos dois lados. Isso reforça que atributos ligados à experiência de lazer/vista/conveniência pesam mais na precificação do que itens de conforto básico já virtualmente padronizados no mercado.
- O status de **superhost** está associado a um ADR mediano 10.8% MENOR que o de hosts comuns, mas com volume de reviews e rating mais altos — um padrão consistente com superhosts precificando de forma mais competitiva (ADR menor) para sustentar alta taxa de ocupação e acumular reviews/reputação, em vez de capturar um prêmio direto de preço.
- Esses dados sustentam uma recomendação operacional para a Seazone: priorizar padronização de amenities de alto impacto e acelerar o caminho até o status de superhost nos imóveis geridos, independentemente do bairro/tamanho escolhido para aquisição.
