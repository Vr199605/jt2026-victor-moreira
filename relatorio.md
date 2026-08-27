# Recomendação de Investimento Imobiliário — Itapema (SC)

**Seazone | Desafio Jovens Talentos AI Builder 2026**

> Análise de dados de short stay (Airbnb), perfis de anfitrião e mercado de compra e venda (VivaReal) para recomendar o melhor perfil de aquisição imobiliária em Itapema/SC, com um business case defensável de um ativo real.

---

## Índice

1. [Resumo Executivo da Recomendação](#1-resumo-executivo-da-recomendação)
2. [A Tese dos Compactos no Centro: Confirmada ou Refutada?](#2-a-tese-dos-compactos-no-centro-confirmada-ou-refutada)
3. [Análise de Bairros, Tipologias e Fatores de Receita](#3-análise-de-bairros-tipologias-e-fatores-de-receita)
4. [Business Case: Ativo Selecionado](#4-business-case-ativo-selecionado)
5. [Riscos e Estratégia de Mitigação](#5-riscos-e-estratégia-de-mitigação)
6. [Metodologia e Bases de Dados](#6-metodologia-e-bases-de-dados)

---

## 1. Resumo Executivo da Recomendação

Cruzamos quatro bases de dados de Itapema (SC) — listings de short stay, perfis de anfitrião, histórico de diárias e mercado de compra e venda — para responder a uma pergunta objetiva: **qual perfil de imóvel maximiza o retorno ajustado a risco para a Seazone?**

**Principais conclusões:**

- A tese interna de que **"compactos no Centro são a aposta mais eficiente" não se confirma** como a melhor opção de Itapema. Compactos no Centro são competitivos *dentro do próprio Centro*, mas o segmento **Morretes / 2 quartos** entrega Net Yield e payback melhores, com ticket de entrada menor e mais estoque disponível.
- O driver de receita mais robusto identificado na base de short stay é a **vista mar** (+30% de ADR mediano), superando comodidades como churrasqueira, vaga de garagem e piscina.
- O status de **superhost está associado a um ADR *menor*** (-10,8%), sugerindo uma estratégia de precificação competitiva para sustentar ocupação e reputação — não um prêmio direto de preço.
- Selecionamos um **ativo real** na base do VivaReal que combina o segmento vencedor (Morretes, 2 quartos) com o driver de maior prêmio comprovado (vista mar), a um preço abaixo da mediana do próprio segmento: **R$ 698.000**, projetando **Net Cap Rate de 8,5% a 9,9%** e **payback de 10 a 12 anos** — superior a qualquer combinação bairro × quartos mapeada.

**Recomendação:** priorizar aquisições no perfil *Morretes, 2 quartos, com vista mar e infraestrutura de lazer*, e não concentrar a estratégia de aquisição em compactos no Centro, cujo estoque disponível é pequeno demais para suportar uma tese de escala.

---

## 2. A Tese dos Compactos no Centro: Confirmada ou Refutada?

**Posição: parcialmente refutada.** Compactos no Centro são um bom ativo, mas não o melhor de Itapema — e o estoque disponível é pequeno demais para uma estratégia de escala.

### 2.1 Comparativo financeiro — cenário base (ocupação 48%)

| Bairro | Faixa de quartos | ADR mediano | Preço mediano | Área mediana | Net Yield | Payback |
|---|---|---:|---:|---:|---:|---:|
| Centro | Compacto (0-1 quarto) | R$ 427 | R$ 895.000 | 53,5 m² | 6,3% | 15,9 anos |
| Centro | 2 quartos | R$ 520 | R$ 1.122.500 | 86,0 m² | 6,1% | 16,4 anos |
| Centro | 3+ quartos | R$ 898,5 | R$ 2.798.800 | 156,0 m² | 4,2% | 23,7 anos |
| Meia Praia | Compacto (0-1 quarto) | R$ 360 | R$ 980.000 | 44,0 m² | 4,8% | 20,7 anos |
| Meia Praia | 2 quartos | R$ 450 | R$ 1.080.000 | 85,0 m² | 5,5% | 18,3 anos |
| Meia Praia | 3+ quartos | R$ 672,7 | R$ 2.499.270 | 153,0 m² | 3,5% | 28,3 anos |
| **Morretes** | **2 quartos** | R$ 400 | R$ 750.000 | 70,0 m² | **7,0%** | **14,3 anos** |
| Morretes | 3+ quartos | n/d* | R$ 840.000 | 105,0 m² | n/d* | n/d* |
| Morretes | Compacto (0-1 quarto) | n/d* | R$ 650.000 | 107,5 m² | n/d* | n/d* |

*n/d: amostra de short stay insuficiente para ADR mediano confiável nesse cruzamento (n < 10 anúncios com diárias válidas).*

### 2.2 Leitura dos dados

**A favor da tese (prós dos compactos no Centro):**
- Maior **receita bruta por m²** de toda a matriz (R$ 1.398/m²/ano), já que o ADR não cai na mesma proporção da redução de área.
- Ticket de aquisição mais baixo em termos absolutos (R$ 895 mil) frente aos demais formatos do Centro.
- Localização central reduz dependência exclusiva de sazonalidade de praia (atrai também hóspedes a trabalho/curta estadia).

**Contra a tese (limitações):**
- **Estoque restrito**: apenas 24 imóveis compactos à venda no Centro na base VivaReal, contra centenas de opções de 2 e 3+ quartos — inviabiliza uma estratégia de aquisição em volume.
- **Amostra pequena de short stay** (103 anúncios) torna o ADR mediano mais sensível a outliers.
- O segmento **Morretes / 2 quartos** entrega Net Yield superior (7,0% vs. 6,3%) e payback menor (14,3 vs. 15,9 anos), com preço de entrada ainda mais baixo (R$ 750 mil vs. R$ 895 mil).

**Conclusão:** compactos no Centro devem permanecer no radar como opção *tática* (bom ativo isolado, boa receita/m²), mas **não devem ser o eixo central da tese de aquisição** da Seazone em Itapema — essa posição cabe ao segmento Morretes/2 quartos, validado na Seção 3 e usado como base do business case (Seção 4).

---

## 3. Análise de Bairros, Tipologias e Fatores de Receita

### 3.1 Bairros e tipologias — visão consolidada

A matriz completa (Seção 2.1) mostra três padrões estruturais:

1. **Apartamentos de 3+ quartos** têm o pior yield em todos os bairros (3,5% a 4,2%) — o preço de aquisição cresce mais rápido que o ADR conforme aumenta o número de quartos, e o payback ultrapassa 22 anos em todos os casos.
2. **Morretes** supera Centro e Meia Praia em yield na faixa de 2 quartos, mesmo com ADR absoluto mais baixo — o motivo é o preço de aquisição significativamente menor (mediana de R$ 750 mil vs. R$ 1,08–1,12 milhão nos demais bairros).
3. **Meia Praia**, apesar de ser o bairro mais consolidado do mercado de short stay em Itapema (maior volume de anúncios e de estoque à venda), tem o pior custo/benefício de aquisição: preços elevados sem ADR proporcionalmente maior.

### 3.2 Fatores que explicam as maiores receitas (drivers de ADR)

Testamos o prêmio de ADR mediano de comodidades e do perfil de anfitrião sobre a base completa de Itapema (anúncios com diária observada válida, n ≈ 991):

| Atributo | ADR mediano (com) | ADR mediano (sem) | Prêmio |
|---|---:|---:|---:|
| **Vista mar** (declarada no anúncio) | R$ 650 | R$ 500 | **+30,0%** |
| Churrasqueira | R$ 598,4 | R$ 485 | +23,4% |
| Vaga de garagem | R$ 575 | R$ 515 | +11,7% |
| Ar-condicionado* | R$ 575 | R$ 400 | +43,8% |
| Piscina | R$ 575 | R$ 575 | 0,0% |

*\*Ar-condicionado tem amostra de comparação não confiável (apenas 12 anúncios de ~991 não têm essa comodidade — a base está praticamente saturada nesse atributo). O sinal estatisticamente mais robusto é o de **vista mar**, com amostra equilibrada (338 com vs. 653 sem).*

| Perfil de anfitrião | ADR mediano | Reviews (mediana) | Rating médio |
|---|---:|---:|---:|
| Superhost | R$ 534 | 26 | 4,92 |
| Host comum | R$ 598,75 | 12 | 4,88 |

**Leitura analítica:**

- **Vista mar é o driver de receita mais confiável de todo o dataset.** Diferente de comodidades de conforto (ar-condicionado, que já é padrão de mercado) ou de lazer condominial (piscina, sem efeito mensurável no ADR), vista mar é um atributo estrutural do imóvel — não pode ser adicionado por reforma, o que também protege o ativo de depreciação relativa frente a lançamentos novos.
- Churrasqueira e vaga de garagem têm prêmios relevantes e mais fáceis de padronizar operacionalmente — bons alvos para investimento incremental em imóveis já adquiridos.
- **Superhost tem ADR menor, não maior.** O padrão sugere que anfitriões com esse status precificam de forma mais competitiva para sustentar ocupação, volume de reviews e reputação — não para capturar um prêmio direto de preço. Para a Seazone, isso reforça o status de superhost como alavanca de **volume e reputação**, não de ADR isolado.

---

## 4. Business Case: Ativo Selecionado

### 4.1 Racional da seleção

Cruzando os dois achados centrais das seções anteriores — (i) o segmento **Morretes / 2 quartos** tem a melhor relação risco-retorno da matriz e (ii) **vista mar** é o driver de receita mais robusto — buscamos na base `VivaReal_Itapema.csv` um imóvel real dentro desse segmento, com esse atributo, e a preço abaixo da mediana do próprio nicho.

### 4.2 Imóvel selecionado

| Campo | Valor |
|---|---|
| **Anúncio** | Apartamento 2 dormitórios (suíte), lazer completo — Morretes, Itapema/SC |
| **ID (VivaReal)** | 2608067036 |
| **Link** | https://www.vivareal.com.br/imovel/apartamento-2-quartos-morretes-bairros-itapema-com-garagem-66m2-venda-RS698000-id-2608067036/ |
| Bairro | Morretes |
| Quartos | 2 (1 suíte) |
| Banheiros | 2 |
| Área útil | 66 m² |
| Vagas de garagem | 1 |
| Comodidades | Piscina, academia, salão de festas, espaço gourmet, playground, piscina infantil, quadra esportiva, elevador, condomínio fechado, portão eletrônico, circuito de segurança, **vista mar**, vista panorâmica |

### 4.3 Preço, custo por m² e custos fixos

| Item | Valor |
|---|---:|
| Preço de aquisição | **R$ 698.000** |
| Custo por m² | R$ 10.576/m² *(≈4,6% abaixo da mediana de Morretes/2q: R$ 11.086/m²)* |
| Condomínio mensal | R$ 350 (R$ 4.200/ano) |
| IPTU anual | R$ 900 |
| **Custos fixos anuais totais** | **R$ 5.100** |

### 4.4 ADR projetado e ocupação

| Parâmetro | Valor | Base |
|---|---:|---|
| ADR mediano do segmento (Morretes/2q, short stay) | R$ 400 | Agregação de dados reais (24 anúncios) |
| Prêmio de vista mar (driver validado) | +30% | 338 vs. 653 anúncios, base completa Itapema |
| **ADR projetado do ativo** | **R$ 520/diária** | ADR do segmento × prêmio de vista mar |
| Ocupação anual estimada | 45% (conservador) / 48% (base) / 52% (otimista) | Faixa realista, litoral catarinense |

O ADR projetado é conservador por construção: aplica **apenas** o prêmio de vista mar, sem somar os prêmios adicionais de churrasqueira/espaço gourmet e infraestrutura de lazer também presentes no imóvel.

### 4.5 DRE simplificada — cenário base (ocupação 48%)

| Linha | Valor | % da Receita |
|---|---:|---:|
| **Receita Bruta Anual** (ADR × Ocupação × 365) | **R$ 91.104** | 100,0% |
| (–) Taxa de gestão Seazone (20%) | R$ 18.221 | 20,0% |
| (–) Manutenção / contingência (5%) | R$ 4.555 | 5,0% |
| (–) Condomínio anual | R$ 4.200 | 4,6% |
| (–) IPTU anual | R$ 900 | 1,0% |
| **OPEX Total** | R$ 27.876 | 30,6% |
| **Receita Líquida Operacional (NOI)** | **R$ 63.228** | 69,4% |
| Gross Cap Rate | **13,1%** | — |
| **Net Cap Rate** | **9,1%** | — |
| **Payback simples** | **≈ 11,0 anos** | — |

### 4.6 Sensibilidade de retorno por ocupação

| Cenário | Ocupação | Receita Bruta | OPEX | NOI | Net Cap Rate | Payback |
|---|---:|---:|---:|---:|---:|---:|
| Conservador | 45% | R$ 85.410 | R$ 26.452 | R$ 58.958 | 8,5% | 11,8 anos |
| **Base** | **48%** | **R$ 91.104** | **R$ 27.876** | **R$ 63.228** | **9,1%** | **11,0 anos** |
| Otimista | 52% | R$ 98.696 | R$ 29.774 | R$ 68.922 | 9,9% | 10,1 anos |

**Leitura:** mesmo no cenário conservador, o Net Cap Rate (8,5%) supera a melhor combinação genérica bairro × quartos da matriz (Morretes/2q "médio", 7,0%), evidenciando o ganho de selecionar o ativo específico certo dentro do segmento certo — e não apenas o bairro/tipologia certos.

---

## 5. Riscos e Estratégia de Mitigação

### Risco 1 — Sazonalidade de inverno (baixa temporada)

Itapema é fortemente sazonal, concentrado em veraneio (dez–mar) e feriados prolongados. Fora de temporada, ocupação e ADR podem cair bem abaixo da média anual usada no modelo.

**Mitigação:**
- Revenue Management dinâmico (precificação por calendário/feriados/eventos regionais) para capturar picos e sustentar ocupação na baixa.
- Diversificar o mix de hóspede para estadias de trabalho/longa duração no inverno — Morretes tem localização mais próxima da BR-101 e menor dependência exclusiva de turismo de praia que Meia Praia.
- Fundo de reserva operacional dimensionado pelos meses de menor ocupação histórica.

### Risco 2 — Liquidez de saída (revenda do ativo)

Morretes tem perfil mais residencial/verticalizado que Meia Praia ou Centro; historicamente pode ter ciclo de venda mais longo em caso de necessidade de desinvestimento.

**Mitigação:**
- Selecionar ativos com infraestrutura de lazer completa e vista mar (como o ativo escolhido), o subsegmento com maior diferenciação e demanda dentro do próprio bairro.
- Manter histórico de performance (ADR, ocupação, reviews) organizado — um argumento comercial forte para revenda a outro investidor.
- Monitorar trimestralmente o volume de estoque à venda no bairro como proxy de liquidez de mercado.

### Risco 3 — Concorrência de novos lançamentos / excesso de oferta

Itapema tem forte atividade de lançamentos; novos empreendimentos com lazer mais moderno podem pressionar ADR de short stay e preço/m² de revenda de imóveis mais antigos.

**Mitigação:**
- Priorizar atributos estruturais e não replicáveis por reforma — vista mar não se deprecia frente a lançamentos novos, diferente de acabamentos/lazer.
- Monitorar continuamente o pipeline de lançamentos na região para antecipar pressão de oferta.
- Padronizar amenities de alto impacto (churrasqueira, vaga de garagem, climatização) e buscar o status de superhost para sustentar competitividade do anúncio frente a estoque novo.

---

## 6. Metodologia e Bases de Dados

| Base | Conteúdo | Uso na análise |
|---|---|---|
| `Details_Itapema.csv` | Listings de short stay (quartos, comodidades, reviews, ratings, owner_id) | Extração de bairro (busca textual), faixa de quartos, drivers de ADR |
| `Hosts_ids_Itapema.csv` | Dados de anfitriões (superhost, tempo de host) | Comparação de ADR por perfil de anfitrião |
| `Price_AV_Itapema.csv` | Histórico diário de preço e disponibilidade | Cálculo de ADR mediano por anúncio (outliers tratados via IQR, k=3) |
| `VivaReal_Itapema.csv` | Mercado de compra e venda (preço, bairro, área, condomínio, IPTU) | Agregação de preço de venda, preço/m² e área por bairro × quartos; seleção do ativo do business case |

**Tratamento de outliers:** diárias e preços de venda tratados pelo método IQR (Tukey), com preços de venda calculados **por bairro** para respeitar diferenças de padrão de mercado regional. Área útil restrita a 15–1000 m² para remover erros grosseiros de digitação.

**Normalização de bairros:** o VivaReal já possui campo estruturado (`suburb`), normalizado por variações de grafia/caixa. O Airbnb não possui esse campo — o bairro foi inferido por busca textual no nome/descrição do anúncio contra a mesma lista canônica de bairros, com uma parcela de anúncios classificada como "não identificado" (tratada à parte, não descartada).

**Premissas financeiras:** ocupação anual em três cenários (45% / 48% / 52%), taxa de gestão Seazone de 20% da receita bruta, manutenção/contingência de 5%, condomínio e IPTU pelos valores reais do imóvel/segmento analisado.

**Limitações conhecidas:**
- Combinações bairro × quartos com poucos anúncios de short stay (n < 10) têm ADR mediano menos confiável e foram sinalizadas como tal.
- O prêmio de ADR de ar-condicionado não é estatisticamente confiável (base quase saturada nessa comodidade).
- O bairro do listing de short stay é inferido textualmente, podendo haver subestimação em anúncios que não mencionam o nome do bairro explicitamente.

---

*Relatório gerado a partir de análise de dados reais de Itapema (SC) — Details_Itapema.csv, Hosts_ids_Itapema.csv, Price_AV_Itapema.csv e VivaReal_Itapema.csv. Scripts completos de limpeza, agregação e modelagem financeira disponíveis no repositório.*
