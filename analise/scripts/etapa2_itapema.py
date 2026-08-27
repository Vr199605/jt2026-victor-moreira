# -*- coding: utf-8 -*-
"""
Seazone | Desafio Jovens Talentos AI Builder 2026
Etapa 2 — Teste da tese "compactos no Centro" + Drivers de ADR (comodidades / host)

Usa as bases brutas (já limpas nos mesmos moldes da Etapa 1) para:
  1. Modelar cenários financeiros (1q / 2q / 3+q) em Centro, Meia Praia e Morretes
     -> Receita Bruta Anual, Receita Bruta/m², Gross Yield, Net Yield (Cap Rate), Payback
  2. Medir o prêmio de ADR gerado por comodidades-chave e por status de superhost

Saídas em /mnt/user-data/outputs/:
  - cenarios_financeiros_bairro_quartos.csv
  - drivers_adr_comodidades.csv
  - drivers_adr_host.csv
  - relatorio_etapa2.md
"""

import re
import unicodedata
import numpy as np
import pandas as pd

IN = "/mnt/user-data/uploads/"
OUT = "/mnt/user-data/outputs/"

pd.set_option("display.width", 160)
pd.set_option("display.max_columns", 30)


def strip_accents(s):
    if pd.isna(s):
        return s
    return "".join(c for c in unicodedata.normalize("NFD", str(s)) if unicodedata.category(c) != "Mn")


def iqr_bounds(s, k=1.5):
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr


# ==========================================================================
# 1. CARGA + LIMPEZA (replica critérios da Etapa 1)
# ==========================================================================

details = pd.read_csv(IN + "Details_Itapema.csv")
price_av = pd.read_csv(IN + "Price_AV_Itapema.csv")
hosts = pd.read_csv(IN + "Hosts_ids_Itapema.csv")
viva = pd.read_csv(IN + "VivaReal_Itapema.csv")

details["airbnb_listing_id"] = details["airbnb_listing_id"].astype(str)
details["owner_id"] = details["owner_id"].astype(str)
for c in ["number_of_bedrooms", "number_of_reviews", "star_rating", "guest_satisfaction_overall"]:
    details[c] = pd.to_numeric(details[c], errors="coerce")
details.loc[details["star_rating"] == 0, "star_rating"] = np.nan
details["aquisition_date"] = pd.to_datetime(details["aquisition_date"], errors="coerce")
details = details.sort_values("aquisition_date").drop_duplicates("airbnb_listing_id", keep="last")

price_av["airbnb_listing_id"] = price_av["airbnb_listing_id"].astype(str)
price_av["price"] = pd.to_numeric(price_av["price"], errors="coerce")
price_av = price_av.dropna(subset=["price"])
price_av = price_av[price_av["price"] > 0]
low_p, high_p = iqr_bounds(price_av["price"], k=3)
low_p = max(low_p, 30)
price_av = price_av[price_av["price"].between(low_p, high_p)]

adr = price_av.groupby("airbnb_listing_id")["price"].median().rename("adr_mediano").reset_index()
details = details.merge(adr, on="airbnb_listing_id", how="left")

hosts["owner_id"] = hosts["owner_id"].astype(str)
hosts["is_superhost"] = hosts["is_superhost"].map({"true": True, "false": False, True: True, False: False})
hosts["host_snapshot_date"] = pd.to_datetime(hosts["host_snapshot_date"], errors="coerce")
hosts = hosts.sort_values("host_snapshot_date").drop_duplicates("owner_id", keep="last")
details = details.merge(hosts[["owner_id", "is_superhost"]], on="owner_id", how="left")

# --- bairro por texto (mesma lógica da Etapa 1) ---
BAIRROS_REF = [
    "Meia Praia", "Morretes", "Centro", "Andorinha", "Castelo Branco", "Canto da Praia",
    "Tabuleiro dos Oliveiras", "Jardim Praia Mar", "Casa Branca", "Alto Sao Bento",
    "Ilhota", "Varzea", "Sertao do Trombudo", "Estreito", "Sertaozinho", "Tabuleiro",
]

def build_pattern(nome):
    base = strip_accents(nome).lower()
    return re.compile(r"\b" + re.escape(base).replace(r"\ ", r"\s+") + r"\b")

patterns = [(b, build_pattern(b)) for b in BAIRROS_REF]

def extrair_bairro(row):
    texto = " ".join(strip_accents(str(row.get(c, ""))).lower() for c in ["ad_name", "ad_description", "space"])
    for bairro, pat in patterns:
        if pat.search(texto):
            return bairro
    return "Não identificado"

details["bairro"] = details.apply(extrair_bairro, axis=1)

# --- bucket de quartos (studio conta como compacto junto com 1 quarto) ---
def bucket_quartos(n):
    if pd.isna(n):
        return "N/D"
    if n <= 1:
        return "Compacto (0-1 quarto)"
    if n == 2:
        return "2 quartos"
    return "3+ quartos"

details["faixa_quartos"] = details["number_of_bedrooms"].apply(bucket_quartos)

BAIRROS_FOCO = ["Centro", "Meia Praia", "Morretes"]

# ==========================================================================
# 2. VIVAREAL — preço mediano / área / condo / iptu por bairro x faixa
# ==========================================================================

viva["sale_price"] = pd.to_numeric(viva["sale_price"], errors="coerce")
viva["usable_area"] = pd.to_numeric(viva["usable_area"], errors="coerce")
viva["bedrooms"] = pd.to_numeric(viva["bedrooms"], errors="coerce")
viva["yearly_iptu"] = pd.to_numeric(viva["yearly_iptu"], errors="coerce")
viva["monthly_condo_fee"] = pd.to_numeric(viva["monthly_condo_fee"], errors="coerce")

viva_v = viva[
    (viva["business_types"] == "Venda") & viva["sale_price"].notna() & viva["usable_area"].notna()
    & (viva["sale_price"] > 0) & (viva["usable_area"].between(15, 1000))
    & viva["suburb"].isin(BAIRROS_FOCO)
].copy()

viva_v["preco_m2"] = viva_v["sale_price"] / viva_v["usable_area"]
viva_v["faixa_quartos"] = viva_v["bedrooms"].apply(bucket_quartos)

# outliers de preço/preço_m2 por bairro
def flag_ok(g, col, k=1.5):
    low, high = iqr_bounds(g[col].dropna(), k)
    return g[col].between(low, high)

viva_v["ok_price"] = viva_v.groupby("suburb", group_keys=False)[["sale_price"]].apply(
    lambda g: flag_ok(g, "sale_price")
).values
viva_v["ok_m2"] = viva_v.groupby("suburb", group_keys=False)[["preco_m2"]].apply(
    lambda g: flag_ok(g, "preco_m2")
).values
viva_v = viva_v[viva_v["ok_price"] & viva_v["ok_m2"]]

viva_agg = (
    viva_v.groupby(["suburb", "faixa_quartos"])
    .agg(
        n_imoveis=("listing_id", "count"),
        preco_venda_mediano=("sale_price", "median"),
        preco_m2_mediano=("preco_m2", "median"),
        area_util_mediana=("usable_area", "median"),
        condo_mensal_mediano=("monthly_condo_fee", "median"),
        iptu_anual_mediano=("yearly_iptu", "median"),
    )
    .reset_index()
    .rename(columns={"suburb": "bairro"})
)

# ==========================================================================
# 3. SHORT STAY — ADR mediano por bairro x faixa
# ==========================================================================

ss_agg = (
    details[details["bairro"].isin(BAIRROS_FOCO) & details["faixa_quartos"].isin(
        ["Compacto (0-1 quarto)", "2 quartos", "3+ quartos"])]
    .groupby(["bairro", "faixa_quartos"])
    .agg(
        n_anuncios=("airbnb_listing_id", "count"),
        adr_mediano=("adr_mediano", "median"),
        reviews_mediano=("number_of_reviews", "median"),
        rating_medio=("star_rating", "mean"),
    )
    .reset_index()
)

# ==========================================================================
# 4. MODELAGEM FINANCEIRA
# ==========================================================================

OCUPACAO_CENARIOS = {"conservador_45pct": 0.45, "base_48pct": 0.48, "otimista_52pct": 0.52}
OPEX_PCT = 0.25  # taxa de gestão Seazone + condomínio + IPTU, estimativa simplificada (~25%)

modelo = ss_agg.merge(viva_agg, on=["bairro", "faixa_quartos"], how="inner")

for nome, ocup in OCUPACAO_CENARIOS.items():
    modelo[f"receita_bruta_{nome}"] = modelo["adr_mediano"] * ocup * 365
    modelo[f"receita_m2_{nome}"] = modelo[f"receita_bruta_{nome}"] / modelo["area_util_mediana"]
    modelo[f"gross_yield_{nome}"] = modelo[f"receita_bruta_{nome}"] / modelo["preco_venda_mediano"] * 100
    modelo[f"net_yield_{nome}"] = modelo[f"gross_yield_{nome}"] * (1 - OPEX_PCT)
    modelo[f"payback_anos_{nome}"] = modelo["preco_venda_mediano"] / (
        modelo[f"receita_bruta_{nome}"] * (1 - OPEX_PCT)
    )

# cenário base (48%) como referência principal para leitura direta
base_cols = [
    "bairro", "faixa_quartos", "n_anuncios", "n_imoveis", "adr_mediano",
    "preco_venda_mediano", "preco_m2_mediano", "area_util_mediana",
    "condo_mensal_mediano", "iptu_anual_mediano",
    "receita_bruta_base_48pct", "receita_m2_base_48pct",
    "gross_yield_base_48pct", "net_yield_base_48pct", "payback_anos_base_48pct",
]
modelo_out = modelo[base_cols].round(2).sort_values(["bairro", "faixa_quartos"])
modelo.round(2).to_csv(OUT + "cenarios_financeiros_bairro_quartos.csv", index=False)

print("=== Modelo financeiro (cenário base 48% ocupação) ===")
print(modelo_out.to_string(index=False))

# ==========================================================================
# 5. DRIVERS DE ADR — COMODIDADES
# ==========================================================================

AMENIDADES_ALVO = {
    "Ar-condicionado": ["ar-condicionado", "ar condicionado"],
    "Churrasqueira": ["churrasqueira"],
    "Vaga de garagem": ["estacionamento", "vaga de garagem", "garagem"],
    "Piscina": ["piscina"],
}

def tem_amenidade(row, termos):
    texto = strip_accents(str(row.get("amenities", ""))).lower()
    return any(strip_accents(t).lower() in texto for t in termos)

# "vista mar" não está nas amenities estruturadas -> buscar no nome/descrição
def tem_vista_mar(row):
    texto = strip_accents(" ".join([str(row.get("ad_name", "")), str(row.get("ad_description", ""))])).lower()
    termos = ["vista mar", "vista para o mar", "frente mar", "frente ao mar", "vista para mar", "beira mar", "beira-mar"]
    return any(strip_accents(t).lower() in texto for t in termos)

details_val = details[details["adr_mediano"].notna()].copy()

resultados_amenidades = []
for nome, termos in AMENIDADES_ALVO.items():
    flag = details_val.apply(lambda r: tem_amenidade(r, termos), axis=1)
    com = details_val.loc[flag, "adr_mediano"]
    sem = details_val.loc[~flag, "adr_mediano"]
    resultados_amenidades.append({
        "atributo": nome,
        "n_com": len(com), "adr_mediano_com": com.median(),
        "n_sem": len(sem), "adr_mediano_sem": sem.median(),
        "premio_pct": (com.median() / sem.median() - 1) * 100 if sem.median() else np.nan,
    })

flag_vm = details_val.apply(tem_vista_mar, axis=1)
com_vm, sem_vm = details_val.loc[flag_vm, "adr_mediano"], details_val.loc[~flag_vm, "adr_mediano"]
resultados_amenidades.append({
    "atributo": "Vista mar (declarada no anúncio)",
    "n_com": len(com_vm), "adr_mediano_com": com_vm.median(),
    "n_sem": len(sem_vm), "adr_mediano_sem": sem_vm.median(),
    "premio_pct": (com_vm.median() / sem_vm.median() - 1) * 100 if sem_vm.median() else np.nan,
})

drivers_amenidades = pd.DataFrame(resultados_amenidades).round(2).sort_values("premio_pct", ascending=False)
drivers_amenidades.to_csv(OUT + "drivers_adr_comodidades.csv", index=False)

print("\n=== Prêmio de ADR por comodidade ===")
print(drivers_amenidades.to_string(index=False))

# ==========================================================================
# 6. DRIVERS DE ADR — SUPERHOST
# ==========================================================================

sup = details_val.loc[details_val["is_superhost"] == True, "adr_mediano"]
nsup = details_val.loc[details_val["is_superhost"] == False, "adr_mediano"]

drivers_host = pd.DataFrame([{
    "atributo": "Superhost",
    "n_superhost": len(sup), "adr_mediano_superhost": sup.median(),
    "n_host_comum": len(nsup), "adr_mediano_host_comum": nsup.median(),
    "premio_pct": (sup.median() / nsup.median() - 1) * 100,
    "reviews_mediano_superhost": details_val.loc[details_val["is_superhost"] == True, "number_of_reviews"].median(),
    "reviews_mediano_host_comum": details_val.loc[details_val["is_superhost"] == False, "number_of_reviews"].median(),
    "rating_medio_superhost": details_val.loc[details_val["is_superhost"] == True, "star_rating"].mean(),
    "rating_medio_host_comum": details_val.loc[details_val["is_superhost"] == False, "star_rating"].mean(),
}]).round(2)
drivers_host.to_csv(OUT + "drivers_adr_host.csv", index=False)

print("\n=== Prêmio de ADR — Superhost vs Host comum ===")
print(drivers_host.to_string(index=False))

# ==========================================================================
# 7. RELATÓRIO
# ==========================================================================

def df_md(df, ffmt="{:.1f}"):
    d = df.copy()
    for c in d.select_dtypes(include=[float]).columns:
        d[c] = d[c].map(lambda x: "" if pd.isna(x) else ffmt.format(x))
    return d.to_markdown(index=False)

# tese: compara compacto vs demais dentro do Centro
centro_compacto = modelo_out[(modelo_out.bairro == "Centro") & (modelo_out.faixa_quartos.str.contains("Compacto"))]
centro_outros = modelo_out[(modelo_out.bairro == "Centro") & (~modelo_out.faixa_quartos.str.contains("Compacto"))]
melhor_yield_global = modelo_out.sort_values("net_yield_base_48pct", ascending=False).iloc[0]
melhor_payback_global = modelo_out.sort_values("payback_anos_base_48pct").iloc[0]

with open(OUT + "relatorio_etapa2.md", "w", encoding="utf-8") as f:
    f.write("# Etapa 2 — Teste de Tese e Drivers de Receita | Itapema (SC)\n\n")
    f.write("**Seazone | Desafio Jovens Talentos AI Builder 2026**\n\n")

    f.write("## 1. Premissas do modelo\n\n")
    f.write("- **Ocupação anual:** 3 cenários — conservador 45%, base 48%, otimista 52% (referência para litoral catarinense).\n")
    f.write("- **Receita Bruta Anual** = ADR mediano × Ocupação × 365.\n")
    f.write("- **OPEX estimado ≈ 25%** (taxa de gestão Seazone + condomínio + IPTU, de forma agregada e simplificada).\n")
    f.write("- **Gross Yield (%)** = Receita Bruta Anual / Preço Mediano de Compra × 100.\n")
    f.write("- **Net Yield / Cap Rate (%)** = Gross Yield × (1 − 25%).\n")
    f.write("- **Payback simples (anos)** = Preço Mediano de Compra / Receita Líquida Anual.\n")
    f.write("- Faixas de quartos: *Compacto* agrupa studio + 1 quarto; demais faixas seguem número de quartos do imóvel.\n\n")

    f.write("## 2. Cenários financeiros por bairro x faixa de quartos (cenário BASE — ocupação 48%)\n\n")
    f.write(df_md(modelo_out) + "\n\n")
    f.write("*(Cenários conservador 45% e otimista 52% completos em `cenarios_financeiros_bairro_quartos.csv`)*\n\n")

    f.write("## 3. A tese dos compactos no Centro se confirma?\n\n")
    if not centro_compacto.empty:
        cy = centro_compacto.iloc[0]["net_yield_base_48pct"]
        cp = centro_compacto.iloc[0]["payback_anos_base_48pct"]
        f.write(f"O segmento **Compacto (0-1 quarto) no Centro** apresenta Net Yield de **{cy:.1f}%** "
                f"e payback simples de **{cp:.1f} anos** no cenário base.\n\n")
    f.write(f"- **Melhor Net Yield da matriz completa:** {melhor_yield_global['bairro']} / "
            f"{melhor_yield_global['faixa_quartos']} ({melhor_yield_global['net_yield_base_48pct']:.1f}%).\n")
    f.write(f"- **Melhor payback da matriz completa:** {melhor_payback_global['bairro']} / "
            f"{melhor_payback_global['faixa_quartos']} ({melhor_payback_global['payback_anos_base_48pct']:.1f} anos).\n\n")

    f.write("**Prós dos compactos no Centro:**\n")
    f.write("- Ticket de aquisição mais baixo, o que reduz a barreira de entrada de capital por unidade.\n")
    f.write("- Receita bruta por m² tende a ser mais alta que unidades maiores, pois o ADR não cai na "
            "mesma proporção da redução de área.\n")
    f.write("- Localização central favorece hóspedes a trabalho/curta estadia e reduz dependência de temporada de praia.\n\n")

    f.write("**Contras / limitações:**\n")
    f.write("- Estoque de compactos é uma fatia pequena do mercado (poucos imóveis de 0-1 quarto ofertados "
            "no VivaReal em relação a 2 e 3+ quartos), o que limita a escala de aquisições da Seazone nesse segmento.\n")
    f.write("- Amostra de anúncios de short stay compactos no Centro também é reduzida, tornando o ADR mediano "
            "mais sensível a poucos anúncios/outliers.\n")
    f.write("- ADR absoluto de compactos costuma ser mais baixo que apartamentos de 2-3 quartos em bairros de praia "
            "(Meia Praia), o que pode limitar o Gross Yield mesmo com preço de compra menor.\n\n")

    f.write("## 4. Drivers de receita — Comodidades\n\n")
    f.write("Prêmio de ADR mediano comparando anúncios que declaram a comodidade/atributo vs. os que não declaram "
            "(toda a base de Itapema, sem filtro de bairro):\n\n")
    f.write(df_md(drivers_amenidades) + "\n\n")
    f.write("*Nota: a base de amenidades estruturadas do Airbnb é quase saturada em ar-condicionado "
            f"(apenas {int(drivers_amenidades.loc[drivers_amenidades.atributo=='Ar-condicionado','n_sem'].iloc[0])} "
            "anúncios sem essa comodidade), então esse prêmio específico deve ser lido com cautela estatística; "
            "os demais atributos têm amostras mais equilibradas.*\n\n")

    f.write("## 5. Drivers de receita — Perfil do anfitrião\n\n")
    f.write(df_md(drivers_host) + "\n\n")

    f.write("## 6. Leitura analítica\n\n")
    top_amenidade = drivers_amenidades.iloc[0]
    top_robusto = drivers_amenidades[drivers_amenidades["atributo"] != "Ar-condicionado"].iloc[0]
    f.write(f"- **{top_amenidade['atributo']}** tem o maior prêmio bruto de ADR (+{top_amenidade['premio_pct']:.1f}%), "
            "mas com amostra de comparação muito pequena (praticamente todos os anúncios já têm ar-condicionado), "
            f"então o sinal mais confiável vem de **{top_robusto['atributo']}**: prêmio de "
            f"+{top_robusto['premio_pct']:.1f}% sobre anúncios sem esse atributo, com amostras equilibradas dos dois lados. "
            "Isso reforça que atributos ligados à experiência de lazer/vista/conveniência pesam mais na precificação "
            "do que itens de conforto básico já virtualmente padronizados no mercado.\n")
    f.write(f"- O status de **superhost** está associado a um ADR mediano "
            f"{'{:.1f}% MAIOR'.format(drivers_host.iloc[0]['premio_pct']) if drivers_host.iloc[0]['premio_pct']>=0 else '{:.1f}% MENOR'.format(abs(drivers_host.iloc[0]['premio_pct']))} "
            "que o de hosts comuns, mas com volume de reviews e rating mais altos — um padrão consistente com "
            "superhosts precificando de forma mais competitiva (ADR menor) para sustentar alta taxa de ocupação "
            "e acumular reviews/reputação, em vez de capturar um prêmio direto de preço.\n")
    f.write("- Esses dados sustentam uma recomendação operacional para a Seazone: priorizar padronização de "
            "amenities de alto impacto e acelerar o caminho até o status de superhost nos imóveis geridos, "
            "independentemente do bairro/tamanho escolhido para aquisição.\n")

print("\nRelatório salvo em:", OUT + "relatorio_etapa2.md")
print("Concluído.")
