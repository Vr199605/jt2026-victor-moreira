# Business Case — Ativo Selecionado para Aquisição | Seazone Itapema (SC)

**Desafio Jovens Talentos AI Builder 2026 — Etapa 3**

---

## 1. Racional da seleção do ativo

Na Etapa 2, o segmento **Morretes / 2 quartos** apresentou a melhor relação risco-retorno de toda a matriz analisada: maior Net Yield (7,0%) e menor payback (14,3 anos) entre bairro × faixa de quartos, com ticket de entrada relativamente baixo (mediana de R$750 mil) frente a Meia Praia e Centro. Também identificamos que **vista mar** é o driver de ADR mais robusto e estatisticamente confiável (+30% de ADR mediano, com amostra equilibrada de 338 vs. 653 anúncios).

Cruzando esses dois achados, buscamos na base `VivaReal_Itapema.csv` um imóvel real dentro do segmento vencedor (Morretes, 2 quartos) que **também** carregasse o atributo de maior prêmio de receita (vista mar), evitando o extremo superior de preço da faixa para não erodir o yield.

### Imóvel selecionado

| Campo | Valor |
|---|---|
| **Anúncio** | "APARTAMENTO 2 DORMITÓRIOS (SUÍTE), LAZER COMPLETO EM ITAPEMA - SC" |
| **ID (VivaReal)** | 2608067036 |
| **Link** | https://www.vivareal.com.br/imovel/apartamento-2-quartos-morretes-bairros-itapema-com-garagem-66m2-venda-RS698000-id-2608067036/ |
| **Anunciante** | LE ATIVA IMÓVEIS |

> **Nota metodológica:** o imóvel foi selecionado por regras objetivas (bairro-alvo, faixa de quartos-alvo, preço próximo à mediana do segmento, presença do driver de maior prêmio comprovado — vista mar) diretamente na base fornecida. Ele deve ser tratado como o **perfil de compra recomendado**, sujeito à checagem de disponibilidade/veracidade do anúncio na due diligence de campo antes da assinatura de qualquer proposta.

---

## 2. Características do imóvel

| Atributo | Valor |
|---|---|
| Bairro | Morretes |
| Quartos | 2 (sendo 1 suíte) |
| Banheiros | 2 |
| Área útil | 66 m² |
| Vagas de garagem | 1 |
| Comodidades declaradas | Piscina, Academia, Salão de festas, Espaço gourmet, Playground, Piscina infantil, Quadra esportiva, Elevador, Condomínio fechado, Portão eletrônico, Circuito de segurança, **Vista mar**, Vista panorâmica |

**Leitura:** o imóvel combina o driver de receita mais robusto identificado na Etapa 2 (vista mar) com infraestrutura de lazer completa (piscina, academia, espaço gourmet/churrasqueira, salão de festas) — atributos que também aparecem entre os de maior prêmio de ADR. Isso posiciona o ativo acima da média de ofertas do próprio segmento Morretes/2 quartos, que tipicamente tem lazer mais básico.

---

## 3. Preço de aquisição e custos fixos

| Item | Valor |
|---|---|
| **Preço de aquisição** | **R$ 698.000** |
| Área útil | 66 m² |
| **Custo por m²** | **R$ 10.576/m²** *(vs. mediana de R$ 11.086/m² em Morretes/2q — ~4,6% abaixo da mediana do segmento)* |
| Condomínio mensal | R$ 350 (R$ 4.200/ano) |
| IPTU anual | R$ 900 |
| Custos fixos anuais totais | R$ 5.100/ano |

O preço/m² está **abaixo** da mediana do próprio segmento (Morretes, 2 quartos), o que reforça a atratividade relativa do ativo mesmo antes de considerar o prêmio de receita da vista mar.

---

## 4. ADR projetado e ocupação

| Parâmetro | Valor | Base |
|---|---|---|
| ADR mediano do segmento (Morretes / 2 quartos, short stay) | R$ 400/diária | Agregação Etapa 2 (short stay real, 24 anúncios) |
| Prêmio de vista mar (driver validado, Etapa 2) | +30% | 338 anúncios com vista mar vs. 653 sem, base completa Itapema |
| **ADR projetado do ativo** | **R$ 520/diária** | ADR do segmento × prêmio de vista mar |
| Ocupação anual estimada | 45% (conservador) / **48% (base)** / 52% (otimista) | Faixa realista para litoral catarinense, Etapa 2 |

O ADR projetado é conservador por construção: aplicamos **apenas** o prêmio de vista mar sobre a mediana do segmento, sem somar os prêmios adicionais de churrasqueira/espaço gourmet e infraestrutura de lazer também presentes no imóvel — que na prática tendem a sustentar um ADR ainda mais alto.

---

## 5. DRE simplificada (projeção anual)

### Cenário BASE — ocupação 48%

| Linha | Valor | % da Receita |
|---|---:|---:|
| **Receita Bruta Anual** (ADR × Ocupação × 365) | **R$ 91.104** | 100,0% |
| (–) Taxa de gestão Seazone (20% da receita) | R$ 18.221 | 20,0% |
| (–) Manutenção / reposição / contingência (5% da receita) | R$ 4.555 | 5,0% |
| (–) Condomínio (anual) | R$ 4.200 | 4,6% |
| (–) IPTU (anual) | R$ 900 | 1,0% |
| **OPEX Total** | R$ 27.876 | 30,6% |
| **Receita Líquida Operacional (NOI)** | **R$ 63.228** | 69,4% |
| Gross Cap Rate (Receita Bruta / Preço) | **13,1%** | — |
| **Net Cap Rate (NOI / Preço)** | **9,1%** | — |
| **Payback simples** | **≈ 11,0 anos** | — |

### Sensibilidade por cenário de ocupação

| Cenário | Ocupação | Receita Bruta | OPEX | NOI | Net Cap Rate | Payback |
|---|---:|---:|---:|---:|---:|---:|
| Conservador | 45% | R$ 85.410 | R$ 26.452 | R$ 58.958 | 8,5% | 11,8 anos |
| **Base** | **48%** | **R$ 91.104** | **R$ 27.876** | **R$ 63.228** | **9,1%** | **11,0 anos** |
| Otimista | 52% | R$ 98.696 | R$ 29.774 | R$ 68.922 | 9,9% | 10,1 anos |

**Leitura:** mesmo no cenário conservador (45% de ocupação), o ativo entrega Net Cap Rate de 8,5% e payback abaixo de 12 anos — superior a qualquer combinação bairro × quartos mapeada na Etapa 2 (a melhor da matriz geral, Morretes 2 quartos "médio", tinha Net Yield de 7,0%). O ganho vem da combinação de (i) preço de compra abaixo da mediana do segmento e (ii) prêmio de ADR por vista mar aplicado de forma conservadora.

---

## 6. Principais riscos e mitigação

### Risco 1 — Sazonalidade de inverno (baixa temporada)
Itapema é um destino fortemente sazonal, concentrado em veraneio (dezembro–março) e feriados prolongados. Fora de temporada, ocupação e ADR podem cair bem abaixo da média anual usada no modelo, pressionando o fluxo de caixa mensal mesmo que a média anual (45-52%) se sustente.

**Mitigação:**
- Precificação dinâmica por Revenue Management (calendário, feriados, eventos regionais) para capturar picos e sustentar ocupação em baixa temporada com descontos direcionados.
- Diversificar o mix de hóspede para incluir estadias de trabalho/longa duração no inverno (nômades digitais, obras/serviços na região), já que Morretes tem localização mais próxima da BR-101 e menos dependência exclusiva de turismo de praia que Meia Praia.
- Reserva de caixa (fundo de reserva operacional) dimensionada pelos meses de menor ocupação histórica, evitando descasamento entre custos fixos (condomínio/IPTU/gestão mínima) e receita sazonal.

### Risco 2 — Liquidez de saída (revenda do ativo)
Morretes é um bairro de perfil mais residencial/verticalizado e menos "trophy asset" que Meia Praia ou Centro; historicamente pode ter ciclo de venda mais longo e menor liquidez em caso de necessidade de desinvestimento rápido.

**Mitigação:**
- Selecionar o ativo dentro de empreendimentos com infraestrutura de lazer completa e vista mar (como o selecionado), que são o subsegmento com maior diferenciação e demanda dentro do próprio bairro, reduzindo o risco de iliquidez.
- Manter documentação e histórico de performance (ADR, ocupação, reviews) do ativo bem organizados, já que um histórico de short stay rentável é um argumento comercial forte tanto para revenda a outro investidor quanto para renegociação.
- Monitorar trimestralmente o volume de estoque à venda no bairro (via VivaReal e portais) como proxy de liquidez de mercado, ajustando o horizonte de saída conforme sinais de excesso de oferta.

### Risco 3 — Concorrência de novos lançamentos / excesso de oferta
Itapema tem forte atividade de lançamentos imobiliários; novos empreendimentos com lazer mais moderno podem pressionar tanto o ADR de short stay quanto o preço/m² de revenda de imóveis mais antigos.

**Mitigação:**
- Priorizar ativos com atributos que não se depreciam rápido frente a lançamentos novos — vista mar é um atributo estrutural (não replicável por reforma), diferente de acabamentos/lazer que podem ficar defasados.
- Monitorar continuamente o pipeline de lançamentos em Morretes e bairros vizinhos (via portais e prefeitura) para antecipar pressão de oferta e ajustar estratégia de precificação/aquisição.
- Investir em padronização de amenities de alto impacto identificadas na Etapa 2 (churrasqueira, vaga de garagem, climatização) e em elevar o anfitrião/gestão ao status de superhost, sustentando competitividade do anúncio mesmo diante de estoque novo na região.

---

## 7. Conclusão

O imóvel selecionado (Morretes, 2 quartos, 66 m², vista mar, lazer completo, R$ 698.000) reúne os dois achados centrais da Etapa 2 — o segmento com melhor risco-retorno da matriz e o driver de receita mais robusto (vista mar) — em um preço abaixo da mediana do próprio segmento. O resultado é um Net Cap Rate projetado de **8,5% a 9,9%** e payback de **10 a 12 anos**, superando todas as demais combinações bairro × quartos mapeadas, com riscos identificados e mitigáveis por meio de gestão ativa de Revenue Management, seleção de ativos diferenciados e monitoramento de mercado — frentes que já fazem parte do modelo de operação da Seazone.
