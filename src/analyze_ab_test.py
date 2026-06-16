import argparse
import re
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "Data",
    "Grupos de usuários",
    "Parceiro",
    "compradores",
    "comissão",
    "cashback",
    "vendas totais",
]


def parse_money_br(value):
    """
    Converte dinheiro em formato brasileiro para float.

    Exemplos aceitos:
    - R$ 10.273
    - R$ 1.234,56
    - 1234.56
    """
    if pd.isna(value):
        return np.nan

    value = str(value).strip()
    value = re.sub(r"[^\d,.\-]", "", value)

    if value == "" or value == "-":
        return np.nan

    if "," in value:
        value = value.replace(".", "").replace(",", ".")
    elif "." in value:
        parts = value.split(".")
        # Caso brasileiro sem centavos: 10.273 = 10273
        if len(parts) > 1 and all(len(part) == 3 for part in parts[1:]):
            value = "".join(parts)

    try:
        return float(value)
    except ValueError:
        return np.nan


def load_dataset(file_path):
    df = pd.read_csv(file_path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")

    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df["compradores"] = pd.to_numeric(df["compradores"], errors="coerce")

    for col in ["comissão", "cashback", "vendas totais"]:
        df[col] = df[col].apply(parse_money_br)

    quality = {
        "linhas_iniciais": len(df),
        "datas_invalidas": int(df["Data"].isna().sum()),
        "compradores_invalidos": int(df["compradores"].isna().sum()),
        "comissao_invalida": int(df["comissão"].isna().sum()),
        "cashback_invalido": int(df["cashback"].isna().sum()),
        "vendas_invalidas": int(df["vendas totais"].isna().sum()),
    }

    df = df.dropna(
        subset=[
            "Data",
            "Grupos de usuários",
            "Parceiro",
            "compradores",
            "comissão",
            "cashback",
            "vendas totais",
        ]
    ).copy()

    quality["linhas_validas"] = len(df)
    quality["linhas_removidas"] = quality["linhas_iniciais"] - quality["linhas_validas"]

    df["lucro_bruto"] = df["comissão"] - df["cashback"]
    df["margem_sobre_gmv"] = np.where(
        df["vendas totais"] > 0,
        df["lucro_bruto"] / df["vendas totais"],
        np.nan,
    )
    df["cashback_rate"] = np.where(
        df["vendas totais"] > 0,
        df["cashback"] / df["vendas totais"],
        np.nan,
    )
    df["comissao_rate"] = np.where(
        df["vendas totais"] > 0,
        df["comissão"] / df["vendas totais"],
        np.nan,
    )
    df["ticket_medio"] = np.where(
        df["compradores"] > 0,
        df["vendas totais"] / df["compradores"],
        np.nan,
    )

    return df, quality


def aggregate_results(df):
    agg = (
        df.groupby(["Parceiro", "Grupos de usuários"])
        .agg(
            dias=("Data", "nunique"),
            compradores_total=("compradores", "sum"),
            compradores_media_dia=("compradores", "mean"),
            comissao_total=("comissão", "sum"),
            cashback_total=("cashback", "sum"),
            vendas_totais=("vendas totais", "sum"),
            lucro_bruto_total=("lucro_bruto", "sum"),
            lucro_bruto_medio_dia=("lucro_bruto", "mean"),
            lucro_bruto_std_dia=("lucro_bruto", "std"),
            margem_sobre_gmv_media=("margem_sobre_gmv", "mean"),
            cashback_rate_medio=("cashback_rate", "mean"),
            comissao_rate_medio=("comissao_rate", "mean"),
            ticket_medio=("ticket_medio", "mean"),
        )
        .reset_index()
    )

    agg["lucro_por_comprador"] = agg["lucro_bruto_total"] / agg["compradores_total"]

    return agg.sort_values("lucro_bruto_medio_dia", ascending=False)


def bootstrap_best_probability(df, metric="lucro_bruto", iterations=10000, seed=42):
    rng = np.random.default_rng(seed)

    groups = sorted(df["Grupos de usuários"].unique())
    values_by_group = {
        group: df.loc[df["Grupos de usuários"] == group, metric].dropna().values
        for group in groups
    }

    wins = {group: 0 for group in groups}
    samples_by_group = {group: [] for group in groups}

    for _ in range(iterations):
        sampled_means = {}

        for group, values in values_by_group.items():
            sample = rng.choice(values, size=len(values), replace=True)
            sampled_mean = sample.mean()
            sampled_means[group] = sampled_mean
            samples_by_group[group].append(sampled_mean)

        best_group = max(sampled_means, key=sampled_means.get)
        wins[best_group] += 1

    probabilities = {
        group: wins[group] / iterations
        for group in groups
    }

    confidence_intervals = {
        group: (
            np.percentile(samples_by_group[group], 2.5),
            np.percentile(samples_by_group[group], 97.5),
        )
        for group in groups
    }

    return probabilities, confidence_intervals


def make_decision(agg, probabilities):
    best = agg.iloc[0]
    best_group = best["Grupos de usuários"]
    groups = list(agg["Grupos de usuários"])

    control_group = "Grupo 1" if "Grupo 1" in groups else groups[0]
    best_probability = probabilities.get(best_group, 0)

    if best["lucro_bruto_total"] <= 0:
        return {
            "resultado": "Sem variante economicamente viável",
            "decisao": "Não escalar aumento de cashback",
            "variante_recomendada": "Nenhuma",
            "racional": "Nenhuma variante apresentou lucro bruto positivo suficiente para justificar escala.",
            "probabilidade": best_probability,
        }

    if best_group == control_group:
        return {
            "resultado": "Controle venceu",
            "decisao": f"Manter {best_group} como padrão e não escalar aumento de cashback",
            "variante_recomendada": best_group,
            "racional": (
                f"O {best_group} teve o maior lucro bruto médio diário e melhor margem. "
                "As variantes com cashback maior trouxeram mais volume em alguns cenários, "
                "mas reduziram o resultado econômico."
            ),
            "probabilidade": best_probability,
        }

    return {
        "resultado": "Vencedor encontrado",
        "decisao": f"Escalar {best_group} para 100% do tráfego",
        "variante_recomendada": best_group,
        "racional": (
            f"O {best_group} apresentou o maior lucro bruto médio diário e probabilidade "
            "suficiente de ser a melhor variante."
        ),
        "probabilidade": best_probability,
    }


def format_currency(value):
    return ("R$ " + f"{value:,.2f}").replace(",", "X").replace(".", ",").replace("X", ".")


def format_percent(value):
    return f"{value * 100:.2f}%".replace(".", ",")


def generate_report(test_name, description, file_path, df, quality, agg, probabilities, confidence_intervals, decision):
    partner = df["Parceiro"].iloc[0]
    start_date = df["Data"].min().date()
    end_date = df["Data"].max().date()

    lines = []

    lines.append(f"# Relatório A/B — {test_name}")
    lines.append("")
    lines.append(f"**Parceiro:** {partner}")
    lines.append(f"**Período:** {start_date} até {end_date}")
    lines.append(f"**Arquivo analisado:** `{file_path}`")
    lines.append("")
    lines.append("## 1. Contexto")
    lines.append("")
    lines.append(description)
    lines.append("")
    lines.append("A pergunta central da análise é: **qual variante de cashback deve ser escalada para 100% do tráfego?**")
    lines.append("")
    lines.append("## 2. Qualidade dos dados")
    lines.append("")
    lines.append(f"- Linhas iniciais: {quality['linhas_iniciais']}")
    lines.append(f"- Linhas válidas: {quality['linhas_validas']}")
    lines.append(f"- Linhas removidas: {quality['linhas_removidas']}")
    lines.append(f"- Datas inválidas: {quality['datas_invalidas']}")
    lines.append(f"- Compradores inválidos: {quality['compradores_invalidos']}")
    lines.append(f"- Comissão inválida: {quality['comissao_invalida']}")
    lines.append(f"- Cashback inválido: {quality['cashback_invalido']}")
    lines.append(f"- Vendas inválidas: {quality['vendas_invalidas']}")
    lines.append("")
    lines.append("## 3. Resultado consolidado por variante")
    lines.append("")
    lines.append("| Grupo | Dias | Compradores | GMV | Comissão | Cashback | Lucro bruto | Lucro médio/dia | Margem GMV | Cashback rate | Lucro/comprador |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")

    for _, row in agg.iterrows():
        lines.append(
            f"| {row['Grupos de usuários']} "
            f"| {int(row['dias'])} "
            f"| {int(row['compradores_total'])} "
            f"| {format_currency(row['vendas_totais'])} "
            f"| {format_currency(row['comissao_total'])} "
            f"| {format_currency(row['cashback_total'])} "
            f"| {format_currency(row['lucro_bruto_total'])} "
            f"| {format_currency(row['lucro_bruto_medio_dia'])} "
            f"| {format_percent(row['margem_sobre_gmv_media'])} "
            f"| {format_percent(row['cashback_rate_medio'])} "
            f"| {format_currency(row['lucro_por_comprador'])} |"
        )

    lines.append("")
    lines.append("## 4. Bootstrap")
    lines.append("")
    lines.append("Foi usada uma simulação bootstrap com a métrica **lucro bruto diário médio**.")
    lines.append("")
    lines.append("| Grupo | Probabilidade de ser o melhor | IC 95% lucro médio/dia |")
    lines.append("|---|---:|---:|")

    for group in sorted(probabilities):
        ci_low, ci_high = confidence_intervals[group]
        lines.append(
            f"| {group} | {format_percent(probabilities[group])} | "
            f"{format_currency(ci_low)} até {format_currency(ci_high)} |"
        )

    lines.append("")
    lines.append("## 5. Decisão")
    lines.append("")
    lines.append(f"**Resultado:** {decision['resultado']}")
    lines.append("")
    lines.append(f"**Decisão:** {decision['decisao']}")
    lines.append("")
    lines.append(f"**Variante recomendada:** {decision['variante_recomendada']}")
    lines.append("")
    lines.append(f"**Racional:** {decision['racional']}")
    lines.append("")
    lines.append("## 6. Leitura executiva")
    lines.append("")
    lines.append(
        "A decisão prioriza lucro bruto e margem, não apenas crescimento de GMV ou compradores. "
        "Cashback maior pode aumentar volume, mas precisa compensar financeiramente. "
        "Neste teste, a recomendação considera eficiência econômica como critério principal."
    )
    lines.append("")
    lines.append("## 7. Limitações")
    lines.append("")
    lines.append(
        "- O dataset não possui visitantes, sessões ou usuários expostos por variante. "
        "Por isso, não é possível calcular taxa de conversão real."
    )
    lines.append("- A análise considera dados agregados por dia e por grupo.")
    lines.append("- Para testes futuros, seria ideal incluir usuários expostos, conversões e segmento de público.")
    lines.append("")

    return "\n".join(lines)


def update_tracker(tracker_path, test_name, description, file_path, df, agg, decision):
    partner = df["Parceiro"].iloc[0]
    groups = ", ".join(sorted(df["Grupos de usuários"].unique()))
    best = agg.iloc[0]

    row = {
        "data_registro": datetime.now().date().isoformat(),
        "nome_teste": test_name,
        "descricao": description,
        "parceiro": partner,
        "periodo_inicio": df["Data"].min().date().isoformat(),
        "periodo_fim": df["Data"].max().date().isoformat(),
        "variantes": groups,
        "resultado": decision["resultado"],
        "decisao": decision["decisao"],
        "variante_recomendada": decision["variante_recomendada"],
        "probabilidade_melhor_variante": round(decision["probabilidade"], 4),
        "lucro_medio_dia_vencedor": round(best["lucro_bruto_medio_dia"], 2),
        "lucro_total_vencedor": round(best["lucro_bruto_total"], 2),
        "margem_gmv_vencedor": round(best["margem_sobre_gmv_media"], 4),
        "arquivo": file_path,
    }

    tracker_path = Path(tracker_path)
    tracker_path.parent.mkdir(parents=True, exist_ok=True)

    if tracker_path.exists():
        tracker = pd.read_csv(tracker_path)
        tracker = pd.concat([tracker, pd.DataFrame([row])], ignore_index=True)
    else:
        tracker = pd.DataFrame([row])

    tracker.to_csv(tracker_path, index=False)


def main():
    parser = argparse.ArgumentParser(description="Analisador reutilizável de teste A/B de cashback.")
    parser.add_argument("--file", required=True, help="Caminho do CSV.")
    parser.add_argument("--test-name", required=True, help="Nome do teste.")
    parser.add_argument("--description", required=True, help="Descrição do teste.")
    parser.add_argument("--tracker", default="outputs/ab_tests_tracker.csv", help="Caminho do tracker CSV.")

    args = parser.parse_args()

    df, quality = load_dataset(args.file)
    agg = aggregate_results(df)
    probabilities, confidence_intervals = bootstrap_best_probability(df)
    decision = make_decision(agg, probabilities)

    report = generate_report(
        test_name=args.test_name,
        description=args.description,
        file_path=args.file,
        df=df,
        quality=quality,
        agg=agg,
        probabilities=probabilities,
        confidence_intervals=confidence_intervals,
        decision=decision,
    )

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    report_name = args.test_name.lower().replace(" ", "_").replace("/", "_")
    report_path = reports_dir / f"{report_name}.md"
    report_path.write_text(report, encoding="utf-8")

    update_tracker(
        tracker_path=args.tracker,
        test_name=args.test_name,
        description=args.description,
        file_path=args.file,
        df=df,
        agg=agg,
        decision=decision,
    )

    print("Análise concluída.")
    print(f"Relatório: {report_path}")
    print(f"Tracker: {args.tracker}")
    print(f"Decisão: {decision['decisao']}")


if __name__ == "__main__":
    main()
