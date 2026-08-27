# -*- coding: utf-8 -*-
"""
Seazone | Desafio Jovens Talentos AI Builder 2026
Etapa 1 — Inspeção, limpeza e cruzamento de dados de Itapema (SC)

Bases:
  1. Details_Itapema.csv    -> listings de short stay (Airbnb)
  2. Hosts_ids_Itapema.csv  -> dados de anfitriões
  3. Price_AV_Itapema.csv   -> histórico diário de preço/disponibilidade
  4. VivaReal_Itapema.csv   -> mercado de compra e venda

Saídas (em /mnt/user-data/outputs/):
  - shortstay_por_anuncio.csv        (ADR mediano, reviews, rating por listing)
  - vivareal_bairro_quartos.csv      (agregação de venda por bairro x quartos)
  - resumo_shortstay_bairro.csv      (agregação de short stay por bairro)
  - relatorio_etapa1.md              (resumo estatístico estruturado)
"""

import re
import unicodedata
import numpy as np
import pandas as pd

pd.set_option("display.width", 140)
pd.set_option("display.max_columns", 30)

IN = "/mnt/user-data/uploads/"
OUT = "/mnt/user-data/outputs/"

# --------------------------------------------------------------------------
# 0. HELPERS
# --------------------------------------------------------------------------

def strip_accents(s: str) -> str:
    if pd.isna(s):
        return s
    return "".join(
        c for c in unicodedata.normalize("NFD", str(s)) if unicodedata.category(c) != "Mn"
    )


def iqr_bounds(series: pd.Series, k: float = 1.5):
    """Retorna limites inferior/superior pelo método IQR (Tukey)."""
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr


def cap_outliers(df: pd.DataFrame, col: str, k: float = 1.5, min_val: float | None = None):
    """Remove outliers de um DataFrame com base no IQR (retorna máscara booleana)."""
    s = df[col].dropna()
    low, high = iqr_bounds(s, k)
    if min_val is not None:
        low = max(low, min_val)
    mask = df[col].between(low, high)
    return mask, low, high


# --------------------------------------------------------------------------
# 1. CARGA E INSPEÇÃO INICIAL
# --------------------------------------------------------------------------

print("Carregando bases...")
details = pd.read_csv(IN + "Details_Itapema.csv")
hosts = pd.read_csv(IN + "Hosts_ids_Itapema.csv")
price_av = pd.read_csv(IN + "Price_AV_Itapema.csv")
viva = pd.read_csv(IN + "VivaReal_Itapema.csv")

print("\n--- Shape bruto ---")
for name, d in [("Details", details), ("Hosts", hosts), ("Price_AV", price_av), ("VivaReal", viva)]:
    print(f"{name}: {d.shape}")

# --------------------------------------------------------------------------
# 2. LIMPEZA — DETAILS (short stay: características do anúncio)
# --------------------------------------------------------------------------

details["airbnb_listing_id"] = details["airbnb_listing_id"].astype(str)
details["owner_id"] = details["owner_id"].astype(str)

num_cols_details = [
    "number_of_bathrooms", "number_of_bedrooms", "number_of_beds", "number_of_guests",
    "number_of_reviews", "cleaning_fee", "star_rating", "picture_count", "min_nights",
    "guest_satisfaction_overall", "accuracy_rating", "checkin_rating", "cleanliness_rating",
    "communication_rating", "location_rating", "value_rating",
]
for c in num_cols_details:
    details[c] = pd.to_numeric(details[c], errors="coerce")

# rating 0.0 nos campos de star_rating normalmente = "sem review ainda" -> tratar como NaN
details.loc[details["star_rating"] == 0, "star_rating"] = np.nan

# remover duplicados de listing_id (mantém o registro mais recente por aquisition_date)
details["aquisition_date"] = pd.to_datetime(details["aquisition_date"], errors="coerce")
details = details.sort_values("aquisition_date").drop_duplicates("airbnb_listing_id", keep="last")

# ------ Extração / normalização de bairro a partir do texto do anúncio ------
BAIRROS_REF = [
    "Meia Praia", "Morretes", "Centro", "Andorinha", "Castelo Branco", "Canto da Praia",
    "Tabuleiro dos Oliveiras", "Jardim Praia Mar", "Casa Branca", "Alto Sao Bento",
    "Ilhota", "Varzea", "Sertao do Trombudo", "Estreito", "Sertaozinho", "Tabuleiro",
]

def build_pattern(nome):
    # ignora acentos/caixa; permite variações de espaço
    base = strip_accents(nome).lower()
    return re.compile(r"\b" + re.escape(base).replace(r"\ ", r"\s+") + r"\b")

patterns = [(b, build_pattern(b)) for b in BAIRROS_REF]

def extrair_bairro(row):
    texto = " ".join(
        strip_accents(str(row.get(c, ""))).lower()
        for c in ["ad_name", "ad_description", "space"]
    )
    for bairro, pat in patterns:
        if pat.search(texto):
            return bairro
    return "Não identificado"

details["bairro"] = details.apply(extrair_bairro, axis=1)

print("\n--- Bairros identificados em Details (short stay) ---")
print(details["bairro"].value_counts())

# --------------------------------------------------------------------------
# 3. LIMPEZA — HOSTS
# --------------------------------------------------------------------------

hosts["owner_id"] = hosts["owner_id"].astype(str)
hosts["is_superhost"] = hosts["is_superhost"].map({"true": True, "false": False, True: True, False: False})
hosts["is_verified"] = hosts["is_verified"].map({"true": True, "false": False, True: True, False: False})
for c in ["number_of_reviews_host", "star_rating_host", "years_host", "months_host"]:
    hosts[c] = pd.to_numeric(hosts[c], errors="coerce")
hosts = hosts.drop_duplicates("owner_id", keep="last")

# --------------------------------------------------------------------------
# 4. LIMPEZA — PRICE_AV (histórico de diária e disponibilidade)
# --------------------------------------------------------------------------

price_av["airbnb_listing_id"] = price_av["airbnb_listing_id"].astype(str)
price_av["price"] = pd.to_numeric(price_av["price"], errors="coerce")
price_av["date"] = pd.to_datetime(price_av["date"], errors="coerce")
price_av = price_av.dropna(subset=["price", "date"])

# diária <= 0 não faz sentido -> descarta
price_av = price_av[price_av["price"] > 0]

# outliers globais de diária (proteção contra erros de digitação/preços absurdos)
mask_price, low_p, high_p = cap_outliers(price_av, "price", k=3, min_val=30)
print(f"\nOutliers de diária (Price_AV): limites [{low_p:.0f}, {high_p:.0f}] "
      f"-> removendo {(~mask_price).sum()} de {len(price_av)} registros")
price_av_clean = price_av[mask_price].copy()

# --------------------------------------------------------------------------
# 5. AGREGAÇÃO SHORT STAY POR ANÚNCIO
# --------------------------------------------------------------------------

adr_by_listing = (
    price_av_clean.groupby("airbnb_listing_id")["price"]
    .agg(adr_mediano="median", adr_medio="mean", n_diarias_observadas="count")
    .reset_index()
)

shortstay = details.merge(adr_by_listing, on="airbnb_listing_id", how="left")
shortstay = shortstay.merge(hosts, on="owner_id", how="left", suffixes=("", "_host"))

cols_shortstay = [
    "airbnb_listing_id", "ad_name", "bairro", "listing_type", "number_of_bedrooms",
    "number_of_bathrooms", "number_of_guests", "adr_mediano", "adr_medio",
    "n_diarias_observadas", "number_of_reviews", "star_rating",
    "guest_satisfaction_overall", "is_superhost", "is_professional",
]
shortstay_out = shortstay[cols_shortstay].copy()
shortstay_out.to_csv(OUT + "shortstay_por_anuncio.csv", index=False)
print(f"\nSalvo: shortstay_por_anuncio.csv ({shortstay_out.shape[0]} anúncios)")

# --------------------------------------------------------------------------
# 6. RESUMO SHORT STAY POR BAIRRO
# --------------------------------------------------------------------------

resumo_bairro_ss = (
    shortstay_out[shortstay_out["bairro"] != "Não identificado"]
    .groupby("bairro")
    .agg(
        n_anuncios=("airbnb_listing_id", "count"),
        adr_mediano=("adr_mediano", "median"),
        reviews_mediano=("number_of_reviews", "median"),
        rating_medio=("star_rating", "mean"),
        pct_superhost=("is_superhost", "mean"),
    )
    .round(2)
    .sort_values("n_anuncios", ascending=False)
    .reset_index()
)
resumo_bairro_ss.to_csv(OUT + "resumo_shortstay_bairro.csv", index=False)

print("\n--- Resumo Short Stay por Bairro ---")
print(resumo_bairro_ss)

# --------------------------------------------------------------------------
# 7. LIMPEZA — VIVAREAL (compra e venda)
# --------------------------------------------------------------------------

viva["sale_price"] = pd.to_numeric(viva["sale_price"], errors="coerce")
viva["usable_area"] = pd.to_numeric(viva["usable_area"], errors="coerce")
viva["bedrooms"] = pd.to_numeric(viva["bedrooms"], errors="coerce")
viva["bathrooms"] = pd.to_numeric(viva["bathrooms"], errors="coerce")
viva["yearly_iptu"] = pd.to_numeric(viva["yearly_iptu"], errors="coerce")
viva["monthly_condo_fee"] = pd.to_numeric(viva["monthly_condo_fee"], errors="coerce")

# manter apenas imóveis à venda com preço e área válidos
# (nota: "listing_type" no VivaReal é o TIPO DE IMÓVEL -- ex.: apartamento, casa;
#  quem indica compra/venda vs. aluguel é "business_types")
viva_venda = viva[
    (viva["business_types"].str.lower() == "venda")
    & viva["sale_price"].notna()
    & viva["usable_area"].notna()
    & (viva["sale_price"] > 0)
    & (viva["usable_area"] > 0)
].copy()

# normalização de bairro (case/acentos/variações)
def normaliza_bairro(s):
    if pd.isna(s):
        return "Não identificado"
    t = strip_accents(str(s)).lower().strip()
    t = re.sub(r"\s+", " ", t)
    mapa = {
        "meia praia": "Meia Praia",
        "meia praia - frente mar": "Meia Praia",
        "morretes": "Morretes",
        "centro": "Centro",
        "andorinha": "Andorinha",
        "castelo branco": "Castelo Branco",
        "canto da praia": "Canto da Praia",
        "tabuleiro dos oliveiras": "Tabuleiro dos Oliveiras",
        "tabuleiro": "Tabuleiro dos Oliveiras",
        "taboleiro": "Tabuleiro dos Oliveiras",
        "jardim praia mar": "Jardim Praia Mar",
        "casa branca": "Casa Branca",
        "alto sao bento": "Alto São Bento",
        "ilhota": "Ilhota",
        "varzea": "Varzea",
        "sertao do trombudo": "Sertão do Trombudo",
        "sertaozinho": "Sertãozinho",
        "estreito": "Estreito",
        "ocean tower": "Meia Praia",  # empreendimento localizado na Meia Praia
        "itapema": "Não identificado",
    }
    return mapa.get(t, str(s).strip().title())

viva_venda["bairro_norm"] = viva_venda["suburb"].apply(normaliza_bairro)

# price/m2
viva_venda["preco_m2"] = viva_venda["sale_price"] / viva_venda["usable_area"]

print("\n--- Bairros normalizados (VivaReal, venda) ---")
print(viva_venda["bairro_norm"].value_counts())

# ------ Outliers de preço de venda e preço/m2 (IQR por bairro) ------
def flag_outlier_iqr(group, col, k=1.5):
    low, high = iqr_bounds(group[col].dropna(), k)
    return group[col].between(low, high)

viva_venda["ok_price"] = viva_venda.groupby("bairro_norm", group_keys=False)[
    ["sale_price"]
].apply(lambda g: flag_outlier_iqr(g, "sale_price")).values
viva_venda["ok_m2"] = viva_venda.groupby("bairro_norm", group_keys=False)[
    ["preco_m2"]
].apply(lambda g: flag_outlier_iqr(g, "preco_m2")).values
# área útil plausível para apto/casa residencial (remove erros grosseiros de digitação)
viva_venda["ok_area"] = viva_venda["usable_area"].between(15, 1000)

n_before = len(viva_venda)
viva_clean = viva_venda[viva_venda["ok_price"] & viva_venda["ok_m2"] & viva_venda["ok_area"]].copy()
print(f"\nOutliers VivaReal removidos: {n_before - len(viva_clean)} de {n_before} "
      f"({(n_before - len(viva_clean)) / n_before:.1%})")

# faixa de quartos (agrupa 4+ para robustez estatística)
viva_clean["faixa_quartos"] = viva_clean["bedrooms"].apply(
    lambda x: "4+" if pd.notna(x) and x >= 4 else (str(int(x)) if pd.notna(x) else "N/D")
)

# --------------------------------------------------------------------------
# 8. AGREGAÇÃO VIVAREAL POR BAIRRO x QUARTOS
# --------------------------------------------------------------------------

agg_viva = (
    viva_clean[viva_clean["bairro_norm"] != "Não identificado"]
    .groupby(["bairro_norm", "faixa_quartos"])
    .agg(
        n_imoveis=("listing_id", "count"),
        preco_venda_mediano=("sale_price", "median"),
        preco_m2_mediano=("preco_m2", "median"),
        area_util_mediana=("usable_area", "median"),
        condo_mediano=("monthly_condo_fee", "median"),
        iptu_mediano=("yearly_iptu", "median"),
    )
    .round(2)
    .reset_index()
    .rename(columns={"bairro_norm": "bairro"})
    .sort_values(["bairro", "faixa_quartos"])
)
agg_viva.to_csv(OUT + "vivareal_bairro_quartos.csv", index=False)

print("\n--- Agregação VivaReal por Bairro x Quartos ---")
print(agg_viva)

# --------------------------------------------------------------------------
# 9. RELATÓRIO ESTRUTURADO (Markdown)
# --------------------------------------------------------------------------

def df_to_md(df, float_fmt="{:.1f}"):
    d = df.copy()
    for c in d.select_dtypes(include=[float]).columns:
        d[c] = d[c].map(lambda x: "" if pd.isna(x) else float_fmt.format(x))
    return d.to_markdown(index=False)

with open(OUT + "relatorio_etapa1.md", "w", encoding="utf-8") as f:
    f.write("# Etapa 1 — Limpeza, Cruzamento e Agregação de Dados | Itapema (SC)\n\n")
    f.write("**Seazone | Desafio Jovens Talentos AI Builder 2026**\n\n")

    f.write("## 1. Volume de dados (bruto vs. limpo)\n\n")
    resumo_vol = pd.DataFrame({
        "Base": ["Details (listings)", "Hosts", "Price_AV (diárias)", "VivaReal (venda)"],
        "Registros brutos": [len(details), len(hosts), len(price_av), len(viva)],
        "Registros após limpeza": [len(shortstay_out), len(hosts), len(price_av_clean), len(viva_clean)],
    })
    f.write(df_to_md(resumo_vol, "{:.0f}") + "\n\n")

    f.write("## 2. Tratamento de outliers\n\n")
    f.write(f"- **Diárias (Price_AV):** método IQR (k=3, limite mínimo R$30) sobre a base completa. "
            f"Faixa aceita: R$ {low_p:.0f} – R$ {high_p:.0f}. "
            f"Removidos {len(price_av) - len(price_av_clean)} registros "
            f"({(len(price_av) - len(price_av_clean)) / len(price_av):.1%}).\n")
    f.write(f"- **Preço de venda e Preço/m² (VivaReal):** método IQR (k=1.5) calculado **por bairro**, "
            f"para respeitar diferenças de padrão de mercado entre regiões. "
            f"Área útil restrita a 15–1000 m². "
            f"Removidos {n_before - len(viva_clean)} registros "
            f"({(n_before - len(viva_clean)) / n_before:.1%}).\n\n")

    f.write("## 3. Normalização de bairros\n\n")
    f.write("- **VivaReal:** variações de grafia/caixa (`meia praia`, `MEIA PRAIA`, `Taboleiro`, etc.) "
            "foram mapeadas para uma lista canônica de bairros de Itapema.\n")
    f.write("- **Airbnb (Details):** não há campo de bairro estruturado; o bairro foi **inferido por "
            "busca textual** (nome + descrição do anúncio) usando a mesma lista canônica do VivaReal. "
            f"Bairro não identificado em {(shortstay_out['bairro']=='Não identificado').mean():.1%} dos anúncios "
            "(tratados à parte, não descartados).\n\n")

    f.write("## 4. Short Stay — resumo por bairro\n\n")
    f.write("ADR mediano (R$/diária), volume mediano de reviews e rating médio, por bairro identificado.\n\n")
    f.write(df_to_md(resumo_bairro_ss, "{:.1f}") + "\n\n")

    f.write("## 5. Venda (VivaReal) — resumo por bairro x nº de quartos\n\n")
    f.write("Preço de venda mediano, preço/m² mediano e área útil mediana, por bairro e faixa de quartos "
            "(imóveis com 4+ quartos agrupados).\n\n")
    f.write(df_to_md(agg_viva, "{:.1f}") + "\n\n")

    f.write("## 6. Observações metodológicas\n\n")
    f.write("- ADR = *Average Daily Rate*, calculado como a mediana das diárias observadas no calendário "
            "de disponibilidade (Price_AV) por anúncio, e depois agregado por bairro.\n")
    f.write("- `star_rating` = 0 foi tratado como ausência de avaliação (NaN), não como nota zero.\n")
    f.write("- Duplicidades de `airbnb_listing_id` e `owner_id` foram removidas mantendo o registro mais recente "
            "(`aquisition_date`).\n")
    f.write("- Apenas imóveis com `business_types == Venda` entraram na agregação de compra e venda "
            "(aluguel tradicional foi excluído do escopo desta etapa).\n")
    f.write(f"- **Atenção:** células da tabela de bairro x quartos com poucas observações "
            f"(n < 10) têm baixa robustez estatística e devem ser interpretadas com cautela — "
            f"há {(agg_viva['n_imoveis'] < 10).sum()} dessas células na tabela completa "
            f"(disponível em `vivareal_bairro_quartos.csv`).\n")

print("\nRelatório salvo em:", OUT + "relatorio_etapa1.md")
print("\nConcluído.")
