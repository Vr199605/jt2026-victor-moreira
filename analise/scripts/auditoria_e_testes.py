# -*- coding: utf-8 -*-
"""
Seazone | Desafio Jovens Talentos AI Builder 2026
Auditoria e Testes de Robustez — consultas ad-hoc feitas durante a análise

Este script consolida as investigações pontuais que sustentam as respostas
dadas na etapa de perguntas de desafio/estresse (ver ai-log/), organizadas
por tema. Cada bloco é independente e pode ser rodado isoladamente.

Pré-requisitos: os CSVs originais em ../data/
"""

import re
import unicodedata
import numpy as np
import pandas as pd

IN = "../data/"
pd.set_option("display.width", 200)


def strip_accents(s):
    if pd.isna(s):
        return s
    return "".join(c for c in unicodedata.normalize("NFD", str(s)) if unicodedata.category(c) != "Mn")


def bairro_do_link(url):
    if pd.isna(url):
        return None
    m = re.search(r"-quartos-([a-z\-]+)-bairros-itapema", url)
    return m.group(1).replace("-", " ").title() if m else None


# ==========================================================================
# TESTE 1 — Preço médio vs. mediano vs. IQR (impacto de outliers/coberturas no Yield)
# ==========================================================================

def teste_1_media_vs_mediana():
    viva = pd.read_csv(IN + "VivaReal_Itapema.csv")
    viva["sale_price"] = pd.to_numeric(viva["sale_price"], errors="coerce")
    viva["usable_area"] = pd.to_numeric(viva["usable_area"], errors="coerce")
    viva["bedrooms"] = pd.to_numeric(viva["bedrooms"], errors="coerce")

    def bucket(n):
        if pd.isna(n):
            return "N/D"
        if n <= 1:
            return "Compacto (0-1 quarto)"
        if n == 2:
            return "2 quartos"
        return "3+ quartos"

    viva["faixa"] = viva["bedrooms"].apply(bucket)
    sub = viva[
        (viva.business_types == "Venda") & viva.sale_price.notna() & viva.usable_area.notna()
        & (viva.sale_price > 0) & (viva.usable_area.between(15, 1000))
        & viva.suburb.isin(["Centro", "Meia Praia", "Morretes"])
        & viva.faixa.isin(["Compacto (0-1 quarto)", "2 quartos", "3+ quartos"])
    ].copy()

    rows = []
    for (bairro, faixa), g in sub.groupby(["suburb", "faixa"]):
        prices = g["sale_price"].dropna()
        q1, q3 = prices.quantile([0.25, 0.75])
        iqr = q3 - q1
        fence = prices[(prices >= q1 - 1.5 * iqr) & (prices <= q3 + 1.5 * iqr)]
        rows.append(dict(
            bairro=bairro, faixa=faixa, n=len(prices),
            media_bruta=prices.mean(), mediana_bruta=prices.median(),
            mediana_fence_iqr=fence.median(), n_fence=len(fence),
        ))
    return pd.DataFrame(rows).sort_values(["bairro", "faixa"])


# ==========================================================================
# TESTE 2 — Validação do campo `suburb` contra o bairro extraído do link_url
# ==========================================================================

def teste_2_validacao_suburb():
    viva = pd.read_csv(IN + "VivaReal_Itapema.csv")
    viva["bairro_link"] = viva["link_url"].apply(bairro_do_link)
    cmp = viva[viva.bairro_link.notna()].copy()
    cmp["match"] = cmp["suburb"].str.strip().str.lower() == cmp["bairro_link"].str.strip().str.lower()
    taxa_divergencia = (~cmp["match"]).mean()
    return taxa_divergencia, cmp[~cmp["match"]][["listing_id", "suburb", "bairro_link", "link_url"]]


# ==========================================================================
# TESTE 3 — Estoque real de "1 quarto no Centro abaixo de R$900 mil"
#           (bairro validado via link_url + filtro anti-comercial)
# ==========================================================================

def teste_3_estoque_centro_1q():
    viva = pd.read_csv(IN + "VivaReal_Itapema.csv")
    viva["sale_price"] = pd.to_numeric(viva["sale_price"], errors="coerce")
    viva["usable_area"] = pd.to_numeric(viva["usable_area"], errors="coerce")
    viva["bedrooms"] = pd.to_numeric(viva["bedrooms"], errors="coerce")
    viva["bairro_link"] = viva["link_url"].apply(bairro_do_link)

    padrao_naoresid = re.compile(r"sala comercial|terreno|loja|galp[aã]o|ponto comercial", re.IGNORECASE)

    base = viva[
        (viva.business_types == "Venda") & viva.sale_price.notna() & (viva.sale_price > 0)
        & viva.usable_area.between(15, 1000)
        & ~viva.listing_title.str.contains(padrao_naoresid, na=False)
    ].copy()

    centro_1q_todos = base[(base.bairro_link == "Centro") & (base.bedrooms == 1)]
    centro_1q_900 = centro_1q_todos[centro_1q_todos.sale_price < 900000]
    return centro_1q_todos, centro_1q_900


# ==========================================================================
# TESTE 4 — Bairro extraído por texto: risco de falso positivo (Details_Itapema)
# ==========================================================================

def teste_4_falso_positivo_bairro_texto():
    details = pd.read_csv(IN + "Details_Itapema.csv")

    TERMOS_PROXIMIDADE = [
        r"a\s+\d+\s*(minutos?|km|quil[oô]metros?)\s+(de|do|da)",
        r"perto\s+(de|do|da)", r"pr[oó]xim[oa]\s+(a|de|do|da)",
        r"a\s+poucos\s+(minutos|metros|passos)\s+(de|do|da)",
    ]
    pat_proximidade = re.compile("|".join(TERMOS_PROXIMIDADE))
    pat_centro = re.compile(r"\bcentro\b")

    def flag(row):
        texto = " ".join(strip_accents(str(row.get(c, ""))).lower() for c in ["ad_name", "ad_description", "space"])
        if not pat_centro.search(texto):
            return None
        pos = pat_centro.search(texto).start()
        janela = texto[max(0, pos - 40):pos]
        return bool(pat_proximidade.search(janela))

    details["suspeita_proximidade"] = details.apply(flag, axis=1)
    validos = details[details.suspeita_proximidade.notna()]
    taxa = validos["suspeita_proximidade"].mean()
    return taxa, len(validos)


# ==========================================================================
# TESTE 5 — Sazonalidade real observada (Price_AV, jan-abr) por bairro
# ==========================================================================

def teste_5_sazonalidade_real():
    details = pd.read_csv(IN + "Details_Itapema.csv")
    price = pd.read_csv(IN + "Price_AV_Itapema.csv")
    details["airbnb_listing_id"] = details["airbnb_listing_id"].astype(str)
    price["airbnb_listing_id"] = price["airbnb_listing_id"].astype(str)
    price["price"] = pd.to_numeric(price["price"], errors="coerce")
    price["date"] = pd.to_datetime(price["date"], errors="coerce")
    price = price.dropna(subset=["price", "date"])
    price = price[price.price > 0]

    BAIRROS_REF = ["Meia Praia", "Morretes", "Centro"]

    def build_pattern(nome):
        base = strip_accents(nome).lower()
        return re.compile(r"\b" + re.escape(base).replace(r"\ ", r"\s+") + r"\b")

    patterns = [(b, build_pattern(b)) for b in BAIRROS_REF]

    def extrair_bairro(row):
        texto = " ".join(strip_accents(str(row.get(c, ""))).lower() for c in ["ad_name", "ad_description", "space"])
        for b, p in patterns:
            if p.search(texto):
                return b
        return "Outro"

    details["bairro"] = details.apply(extrair_bairro, axis=1)
    merged = price.merge(details[["airbnb_listing_id", "bairro"]], on="airbnb_listing_id", how="left")
    merged["month"] = merged.date.dt.month
    return merged.groupby(["bairro", "month"])["price"].median().unstack()


# ==========================================================================
# TESTE 6 — Payback descontado (11% a.a.) — perpetuidade de NOI constante
# ==========================================================================

def teste_6_payback_descontado(preco, noi_anual, taxa=0.11):
    net_yield = noi_anual / preco
    if net_yield > taxa:
        n = -np.log(1 - preco * taxa / noi_anual) / np.log(1 + taxa)
        return dict(converge=True, anos=n)
    valor_perpetuidade = noi_anual / taxa
    return dict(converge=False, deficit=preco - valor_perpetuidade, deficit_pct=(preco - valor_perpetuidade) / preco)


# ==========================================================================
# TESTE 7 — Superhost: ADR vs. velocidade de reviews normalizada por tenure
# ==========================================================================

def teste_7_superhost_cac():
    details = pd.read_csv(IN + "Details_Itapema.csv")
    hosts = pd.read_csv(IN + "Hosts_ids_Itapema.csv")
    price = pd.read_csv(IN + "Price_AV_Itapema.csv")

    details["airbnb_listing_id"] = details["airbnb_listing_id"].astype(str)
    details["owner_id"] = details["owner_id"].astype(str)
    hosts["owner_id"] = hosts["owner_id"].astype(str)
    price["airbnb_listing_id"] = price["airbnb_listing_id"].astype(str)
    price["price"] = pd.to_numeric(price["price"], errors="coerce")
    price = price.dropna(subset=["price"])
    price = price[price.price > 0]
    q1, q3 = price["price"].quantile([0.25, 0.75])
    iqr = q3 - q1
    low, high = max(q1 - 3 * iqr, 30), q3 + 3 * iqr
    price_clean = price[price.price.between(low, high)]
    adr = price_clean.groupby("airbnb_listing_id")["price"].median().rename("adr_mediano").reset_index()
    details = details.merge(adr, on="airbnb_listing_id", how="left")

    hosts["is_superhost"] = hosts["is_superhost"].map({"true": True, "false": False, True: True, False: False})
    hosts["years_host"] = pd.to_numeric(hosts["years_host"], errors="coerce")
    hosts["months_host"] = pd.to_numeric(hosts["months_host"], errors="coerce")
    hosts["host_snapshot_date"] = pd.to_datetime(hosts["host_snapshot_date"], errors="coerce")
    hosts = hosts.sort_values("host_snapshot_date").drop_duplicates("owner_id", keep="last")
    hosts["tenure_meses"] = hosts["years_host"] * 12 + hosts["months_host"]
    details = details.merge(hosts[["owner_id", "is_superhost", "tenure_meses"]], on="owner_id", how="left")
    details["number_of_reviews"] = pd.to_numeric(details["number_of_reviews"], errors="coerce")

    d = details[details.adr_mediano.notna() & details.is_superhost.notna() & (details.tenure_meses > 0)].copy()
    d["reviews_por_mes_tenure"] = d["number_of_reviews"] / d["tenure_meses"]
    return d.groupby("is_superhost").agg(
        tenure_mediano=("tenure_meses", "median"),
        adr_mediano=("adr_mediano", "median"),
        reviews_mediano=("number_of_reviews", "median"),
        velocidade_reviews=("reviews_por_mes_tenure", "median"),
    )


if __name__ == "__main__":
    print("=== Teste 1: Média vs. Mediana vs. IQR (impacto no preço de compra) ===")
    print(teste_1_media_vs_mediana(), "\n")

    print("=== Teste 2: Validação do campo suburb vs. link_url ===")
    taxa, divergentes = teste_2_validacao_suburb()
    print(f"Taxa de divergência: {taxa:.1%} ({len(divergentes)} registros)\n")

    print("=== Teste 3: Estoque real de 1 quarto no Centro ===")
    todos, abaixo_900k = teste_3_estoque_centro_1q()
    print(f"Total 1q Centro (residencial, bairro validado): {len(todos)}")
    print(f"Abaixo de R$900 mil: {len(abaixo_900k)}\n")

    print("=== Teste 4: Falso positivo na extração textual de 'Centro' ===")
    taxa_fp, n_val = teste_4_falso_positivo_bairro_texto()
    print(f"Taxa de menção por proximidade: {taxa_fp:.1%} (n={n_val})\n")

    print("=== Teste 5: Sazonalidade real por bairro (jan-abr) ===")
    print(teste_5_sazonalidade_real(), "\n")

    print("=== Teste 6: Payback descontado (ativo selecionado, cenário sazonal) ===")
    print(teste_6_payback_descontado(preco=698000, noi_anual=40530), "\n")

    print("=== Teste 7: Superhost — ADR vs. velocidade de reviews ===")
    print(teste_7_superhost_cac())
