# AI Log — Desafio Jovens Talentos AI Builder 2026 (Itapema/SC)

Registro do processo de análise assistido por IA (Claude, Anthropic). Este log documenta
a sequência de prompts usados para conduzir, testar e estressar a análise, junto com a
síntese de cada resposta. O detalhamento numérico completo de cada etapa está em
`../relatorio.md`; aqui o objetivo é registrar o *processo* — o que foi perguntado, por quê,
e o que mudou na análise como resultado.

---

## Etapa 1 — Inspeção, limpeza e cruzamento das 4 bases

**Prompt:** pedido de script Python para inspecionar, limpar e cruzar `Details_Itapema.csv`,
`Hosts_ids_Itapema.csv`, `Price_AV_Itapema.csv` e `VivaReal_Itapema.csv`; tratar outliers de
preço; normalizar bairros em ambos os datasets; agregar ADR mediano/reviews/rating por
anúncio e preço de venda/R$-m²/área por bairro × quartos.

**Resultado:** `scripts/etapa1_itapema.py`. Decisões-chave: outliers de diária via IQR
(k=3, piso R$30) na base completa; outliers de preço de venda via IQR (k=1,5) **por bairro**;
bairro do VivaReal normalizado a partir do campo `suburb`; bairro do Airbnb inferido por
busca textual (campo `suburb` não existe em `Details_Itapema.csv`).

---

## Etapa 2 — Modelagem financeira e drivers de ADR

**Prompt:** modelar cenários financeiros (1 quarto vs. 2 vs. 3+) em Centro/Meia Praia/Morretes
com ocupação 45-52%, calculando Receita Bruta, Yield, Net Yield (OPEX ~25%) e Payback;
identificar quais comodidades e qual perfil de anfitrião geram maior prêmio de ADR.

**Resultado:** `scripts/etapa2_itapema.py`. Achados centrais: tese de "compactos no Centro"
não se confirma como melhor opção (Morretes/2q vence em yield); vista mar é o driver de ADR
mais robusto (+30%); superhost tem ADR **menor**, não maior (-10,8%).

**Bug corrigido no processo:** esquecimento de deduplicar `Hosts_ids_Itapema.csv` por
`owner_id` gerou explosão de linhas por merge (owner com até 112 registros duplicados) —
identificado porque as contagens de anúncios por segmento ficaram maiores que o total da
base. Corrigido com `drop_duplicates('owner_id', keep='last')`.

---

## Etapa 3 — Business case do ativo selecionado

**Prompt:** selecionar um imóvel real na base VivaReal que maximize risco/retorno, montar
DRE simplificada (Receita, OPEX, NOI, Net Cap Rate, Payback) e listar 3 riscos com mitigação.

**Resultado:** ativo selecionado — Morretes, 2 quartos, 66m², vista mar, R$698.000
(ID VivaReal 2608067036), escolhido por cruzar o segmento vencedor (Morretes/2q) com o
driver de receita mais robusto (vista mar), a preço abaixo da mediana do próprio segmento.

---

## Perguntas de desafio e estresse (com efeito na análise)

| # | Pergunta | O que mudou na análise |
|---|---|---|
| 1 | OPEX flat de 25% ignora que condomínio/IPTU pesam mais em compactos? | Recalculado com gestão variável (20%) + custos fixos reais; Net Yield do compacto do Centro caiu 0,32 p.p., o de Morretes/2q subiu 0,38 p.p. |
| 2 | Preço médio do VivaReal está puxado por coberturas frente-mar? | Confirmado: usar média bruta em vez de mediana+IQR inverteria a conclusão (compactos pareceriam os piores ativos, não os melhores). Método mediana+IQR mantido como correto. |
| 3 | Ocupação anual flat esconde sazonalidade (alta/baixa)? | Modelo de 2 regimes construído (90 dias/75% vs. 275 dias/30%, -40% ADR); validado contra queda real jan→abr na base. Receita projetada caiu 33%. |
| 4 | Payback descontado a 11% (CDI/Selic)? | Net Yield (5,8-9,1%) < taxa de desconto em ambos os cenários → payback descontado **não converge** via renda pura; retorno depende de valorização do imóvel. |
| 5 | Meia Praia concentra >60% dos anúncios — Centro tem mais risco de vacância? | Não: Meia Praia (80% do estoque) tem queda sazonal de ADR maior (-42,9% vs. -33,5%) e menos reviews por anúncio — mais exposta a demanda monotemática. |
| 6 | Foco em compactos ignora que famílias de 4-6 pessoas dominam o turismo de SC? | Confirmado por dados de capacidade: 2 quartos tem 86,6% dos anúncios dimensionados para 4-6 hóspedes; reforça a escolha por Morretes/2q em vez de compacto. |
| 7 | Quantos anúncios reais de 1 quarto existem no Centro abaixo de R$900 mil? | Apenas 8 (após validar bairro via `link_url`, já que o campo `suburb` tem 19,9% de divergência) — estoque insuficiente para escala. |
| 8 | Coordenadas lat/lon zeradas — como validar a extração textual de bairro? | Confirmado 100% zerado. Auditoria identificou ~35,8% de risco de falso positivo em "Centro" por colisão de palavra-chave + linguagem de proximidade. |
| 9 | Filtros de saneamento para área útil errada (ex.: 4.000 m² em imóvel de 1 quarto)? | Filtro [15,1000] m² já capturava o erro; achado adicional: 15 imóveis comerciais/terrenos mal cadastrados como residenciais, com filtro de palavra-chave proposto. |
| 10 | Ar-condicionado com ADR menor é Simpson's Paradox? | Correção de premissa: ADR do AC é maior (+43,8%), não menor. Investigação da amostra pequena (12 "sem AC") encontrou 2 casos de imóveis de luxo mal cadastrados — prêmio real provavelmente subestimado, não superestimado. |
| 11 | Superhost: ganho é em ADR ou em CAC/conversão? | Confirmado CAC/conversão: velocidade de reviews normalizada por tenure é 2,6x maior em superhosts, mesmo com contas mais novas (não mais antigas). |
| 12 | Vaga de garagem muda ADR entre 1 e 3 quartos? 2 vagas geram prêmio real? | Sim: 2ª vaga gera +17-18% de ADR em 2q/3q+ (perfil rodoviário PR/RS); irrelevante em compactos (quase não há oferta de 2 vagas nesse formato). |
| 13 | Risco de canibalização por novos lançamentos de estúdios (24 meses)? | Compactos são 2,4% do estoque mas 4,5% do pipeline de lançamentos identificado (quase 2x sobre-representados), concentrados em Morretes e Meia Praia. |
| 14 | Liquidez de revenda: 2q Meia Praia vs. compacto Centro, horizonte de 3 anos? | Meia Praia tem liquidez muito maior (392 vs. 16 imóveis em estoque; 81 vs. 15 agentes; dispersão de preço metade). |

---

## Observações sobre o processo

- Todos os números reportados nas respostas de estresse foram recalculados a partir dos
  CSVs originais em cada resposta (não reaproveitados de memória), o que permitiu capturar
  o bug de deduplicação de hosts (item acima) antes de virar erro na entrega final.
- Onde a pergunta do usuário continha uma premissa numérica incorreta (perguntas 10 e a
  citação "diárias médias apenas ligeiramente superiores" na pergunta do superhost), a IA
  corrigiu o dado publicamente antes de responder, em vez de aceitar a premissa como fato.
- A limitação de dado mais material identificada ao longo de todo o processo foi a
  cobertura temporal de `Price_AV_Itapema.csv` (jan-abr apenas) — sinalizada como risco
  residual mesmo após o ajuste de sazonalidade (pergunta 3).
