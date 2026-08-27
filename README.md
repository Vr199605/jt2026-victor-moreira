[Link do Vídeo de Apresentação (Google Drive)](https://drive.google.com/file/d/1uW8DKH_cD7lL-2NwM-3VU5fI1V_EA2Kp/view?usp=sharing) — *acesso público configurado ("Qualquer pessoa com o link")*

[Link da Transcrição do Vídeo (Google Drive)](https://drive.google.com/file/d/1o1g-TjaBx8MDRIMpwR5NR6XOpqYzSSEo/view?usp=sharing)

[Link de apresentação pptx](https://docs.google.com/presentation/d/1PeKNgerrr_854qG8rQO-GISdIQWZdpm9/edit?usp=sharing&ouid=114215544640110980972&rtpof=true&sd=true)

# Recomendação de Investimento Imobiliário — Itapema (SC)

**Desafio Jovens Talentos AI Builder 2026 | Seazone**
Análise de dados de short stay (Airbnb), perfis de anfitrião, histórico de diárias e mercado de compra e venda para recomendar o perfil ótimo de aquisição imobiliária em Itapema/SC.

📊 **Slides da apresentação:** [`apresentacao/apresentacao.pptx`](./apresentacao/apresentacao.pptx)

---

## Índice

1. [Resumo Executivo & Recomendação de Investimento](#1-resumo-executivo--recomendação-de-investimento)
2. [Posicionamento sobre a Tese Interna (Compactos no Centro)](#2-posicionamento-sobre-a-tese-interna-compactos-no-centro)
3. [Diagnóstico de Mercado e Drivers de Receita](#3-diagnóstico-de-mercado-e-drivers-de-receita)
4. [Tratamento Metodológico, Dados e Gestão de Riscos](#4-tratamento-metodológico-dados-e-gestão-de-riscos)
5. [Reprodutibilidade & Arquitetura do Projeto](#5-reprodutibilidade--arquitetura-do-projeto)
6. [Próximos Passos](#6-próximos-passos-se-tivéssemos-mais-1-semana)

---

## 1. Resumo Executivo & Recomendação de Investimento

### Recomendação

> **Adquirir um apartamento de 2 quartos em Morretes, com vista mar e infraestrutura de lazer completa, na faixa de R$ 650 mil a R$ 750 mil (mediana de mercado: R$ 750.000; preço/m² alvo: ~R$ 10.500–11.100/m²).**

Esse perfil combina o segmento com **melhor relação risco-retorno de toda a matriz bairro × tipologia** analisada com o **driver de ADR mais robusto identificado na base** (vista mar, +30%), a um preço abaixo da mediana do próprio nicho. O ativo específico usado como referência do business case (ID VivaReal 2608067036 — 66 m², 2 suítes, R$ 698.000) está detalhado no `relatorio.md`.

### KPIs de retorno — ativo de referência

| KPI | Modelo ingênuo (ocupação flat 48%) | **Modelo validado (sazonal)** |
|---|---:|---:|
| Preço de Aquisição | R$ 698.000 | R$ 698.000 |
| ADR estimado | R$ 520 (fixo o ano todo) | R$ 520 (alta) / R$ 312 (baixa, -40%) |
| Ocupação anual ponderada | 48% | **41,1%** |
| Receita Bruta Anual | R$ 91.104 | **R$ 60.840** |
| OPEX (gestão 20% + manutenção 5% + condomínio + IPTU reais) | R$ 27.876 (30,6%) | R$ 20.310 (33,4%) |
| **NOI** | R$ 63.228 | **R$ 40.530** |
| Gross Yield | 13,1% | 8,7% |
| **Net Cap Rate** | 9,1% | **5,8%** |
| **Payback Simples** | 11,0 anos | **17,2 anos** |
| **Payback Descontado (11% a.a.)** | Não converge* | **Não converge*** |

*\*Net Cap Rate inferior à taxa de desconto em ambos os cenários — o retorno total depende de valorização do imóvel na revenda, não apenas do fluxo de aluguel (detalhamento na Seção 4).*

**Leitura executiva:** o modelo ingênuo superestima a receita em ~33%. O modelo validado é mais conservador, mas ainda supera qualquer outra combinação bairro × tipologia mapeada nesta análise.

---

## 2. Posicionamento sobre a Tese Interna (Compactos no Centro)

### Veredito

> **A tese não se sustenta como estratégia central de aquisição — apenas como posição tática pontual, com ressalva explícita de escala e liquidez.**

### Tabela comparativa de rentabilidade (Net Yield ajustado pela assimetria real de custos fixos)

| Tipologia / Bairro | ADR mediano | Preço mediano | Receita Bruta/m²/ano | Condo+IPTU (% receita) | **Net Yield real** | Payback |
|---|---:|---:|---:|---:|---:|---:|
| **1 Quarto — Centro** | R$ 427 | R$ 895.000 | **R$ 1.398** (maior) | 8,8% (maior) | 5,95% | 15,9 anos |
| 2 Quartos — Meia Praia | R$ 450 | R$ 1.080.000 | R$ 927 | 7,7% | 5,28% | 18,9 anos |
| 3 Quartos — Meia Praia | R$ 673 | R$ 2.499.270 | R$ 742 | 5,2% | 3,53% | 28,3 anos |
| 3 Quartos — Centro | R$ 899 | R$ 2.798.800 | R$ 1.009 | 0,0%** | 4,50% | 22,2 anos |
| **2 Quartos — Morretes** *(recomendado)* | R$ 400 | R$ 750.000 | R$ 1.001 | **0,9%** (menor) | **7,39%** (maior) | **13,5 anos** (menor) |

*\*\*Sem condomínio/IPTU reportado no anúncio — tratado como zero por padrão conservador.*

### Receita por m² vs. limitação de estoque

| Métrica de escala | 1 Quarto — Centro | 2 Quartos — Meia Praia |
|---|---:|---:|
| Estoque residencial total (bairro validado via URL) | **17 unidades** | 392 unidades |
| Estoque abaixo de R$ 900 mil | **8 unidades** | — |
| Imobiliárias/anunciantes distintos | 15 | 81 |
| Dispersão de preço (coef. de variação) | 0,64 | 0,30 |

O compacto do Centro vence em receita/m² (R$1.398, a maior da matriz), mas com só 17 unidades residenciais no bairro inteiro (8 abaixo de R$900 mil), a Seazone precisaria comprar praticamente todo o estoque para montar portfólio — inviável em escala. **Conclusão: bom ativo isolado, péssima base para tese de volume.**

---

## 3. Diagnóstico de Mercado e Drivers de Receita

### Melhor localização — receita, volume e liquidez

| Critério | Meia Praia | Centro | Morretes |
|---|---|---|---|
| Share do estoque de short stay | **80,0%** | 16,1% | 1,6% |
| Queda de ADR alta→baixa temporada | **-42,9%** (mais sazonal) | -33,5% | -33,3% |
| Reviews medianos por anúncio | 2,0 | **3,0** | 1,0 |
| Net Yield do melhor segmento local | 5,5% | 6,3% | **7,4%** |
| Liquidez de revenda | Alta (392 imóveis, 81 agentes) | Baixa (17 imóveis, 15 agentes) | Não mapeada |

### Comodidades que geram prêmio de ADR

| Comodidade | Prêmio de ADR | Confiabilidade |
|---|---:|---|
| **Vista mar** | **+30,0%** | **Alta** (338 vs. 653) |
| Churrasqueira | +23,4% | Alta |
| 2ª vaga de garagem (2q/3q+) | +17,6% a +18,3% | Alta |
| Ar-condicionado | +43,8% (até +82,5% corrigido) | **Baixa** (amostra saturada) |
| Piscina | +0,0% | Alta — sem efeito |

### Perfil de gestão: Superhost — conversão, não preço

| Métrica (normalizada por tenure) | Host comum | Superhost | Múltiplo |
|---|---:|---:|---:|
| ADR mediano | R$ 598 | R$ 534 | **-10,8%** |
| Tempo de casa (mediano) | 71,0 meses | 58,5 meses | Superhost tem *menos* |
| Reviews por mês de tenure | 0,248 | **0,654** | **2,6x** |
| Receita-proxy por mês | R$ 137,5 | **R$ 327,4** | **2,4x** |

Superhosts precificam abaixo do mercado, mas giram 2,6x mais rápido — ganho real em **conversão/redução de CAC**, não em ADR.

---

## 4. Tratamento Metodológico, Dados e Gestão de Riscos

### Saneamento de dados

| Problema | Tratamento |
|---|---|
| Outliers de área (1 quarto com 4.000+ m²) | Filtro `usable_area` entre 15–1.000 m² |
| Outliers de preço/R$m² | IQR (k=1,5) **por bairro** |
| Outliers de diária | IQR (k=3, piso R$30) na base completa |
| Salas comerciais cadastradas como `bedrooms=1` | Filtro por palavra-chave no título — removeu 15 registros |
| Campo `suburb` não confiável | Validação via `link_url` — **divergência de 19,9%** |
| **Coordenadas lat/lon zeradas (100% da base)** | Bairro inferido por busca textual; auditoria identificou **~35,8%** de risco de falso positivo em "Centro" (colisão de palavra + proximidade) — **maior limitação de dado da análise** |

### Ajuste de sazonalidade

`Price_AV_Itapema.csv` cobre só jan-abr/2025. Modelo de 2 regimes construído (Alta: Dez-Fev, 90 dias, 75% ocup.; Baixa: Mar-Nov, 275 dias, 30% ocup., -40% ADR), validado contra a queda real observada (Jan R$800 → Abr R$480 = -40%). Reduz receita projetada em 33% vs. modelo flat. Limitação residual: desconto calibrado só com dados de outono, inverno pleno pode ser ainda mais fraco.

### Assimetria de OPEX por tipologia

| Tipologia | Condo+IPTU (% da receita) |
|---|---:|
| Centro — Compacto | **8,8%** (maior) |
| Meia Praia — 2q | 7,7% |
| **Morretes — 2q** | **0,9%** (menor) |

### Riscos mapeados

| Risco | Evidência | Mitigação |
|---|---|---|
| Vacância em baixa temporada | Net Cap Rate cai de 9,1% para 5,8% ao sazonalizar | Revenue Management dinâmico; diversificação para estadias longas no inverno |
| Liquidez de revenda | Payback descontado a 11% não converge via renda pura | Priorizar bairros com estoque/agentes profundos; documentar histórico de performance |
| Concorrência de lançamentos | Compactos são 2,4% do estoque mas 4,5% do pipeline de lançamentos | Priorizar atributos estruturais (vista mar); monitorar pipeline nos bairros-alvo |

---

## 5. Reprodutibilidade & Arquitetura do Projeto

```
itapema-investment-analysis/
├── README.md
├── relatorio.md                       # relatório completo de análise e recomendação final
├── apresentacao/
│   └── apresentacao.pptx              # slides (vídeo linkado no topo deste README)
├── analise/
│   ├── data/                          # os 4 CSVs originais
│   ├── scripts/
│   │   ├── etapa1_itapema.py          # limpeza, cruzamento e agregação
│   │   ├── etapa2_itapema.py          # modelagem financeira e drivers de ADR
│   │   └── auditoria_e_testes.py      # consultas de validação e testes de robustez
│   └── outputs/                       # planilhas de apoio já geradas
└── ai-log/
    └── conversa-analise-itapema.md    # registro do processo de análise assistido por IA
```

### Como executar

```bash
pip install pandas numpy tabulate --break-system-packages

cd analise/scripts
python3 etapa1_itapema.py        # limpeza, normalização de bairros, agregações
python3 etapa2_itapema.py        # modelagem financeira e drivers de ADR
python3 auditoria_e_testes.py    # consultas de validação (perguntas de estresse)
```

Os scripts leem os CSVs de `../data/` e imprimem/salvam os resultados agregados. Os arquivos já gerados estão em `analise/outputs/` para consulta direta. Não é necessária nenhuma API externa ou credencial.

---

## 6. Próximos Passos (Se tivéssemos mais 1 semana)

1. **Regressão hedônica para precificação dinâmica**, isolando o efeito de cada comodidade controlando simultaneamente por bairro, tipologia e sazonalidade.
2. **Geocodificação real via API** (Google Maps/Nominatim) para resolver as coordenadas zeradas e calcular distância exata até o mar.
3. **Scraping de lançamentos imobiliários** (sites de construtoras/prefeitura) para um calendário real de entregas nos próximos 24 meses.
4. **Dados de ocupação/reserva reais**, substituindo `number_of_reviews` como proxy de demanda.
5. **Cobertura sazonal completa** (dados de inverno pleno, jun-ago), substituindo a extrapolação atual do desconto de baixa estação.
