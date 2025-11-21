import streamlit as st
import pandas as pd
from utils.crud import select
import plotly.graph_objects as go

CORES = {
    "receitas": "#2ecc71",
    "não atribuído": "#3498db",
    "despesas essenciais": "#e74c3c",
    "despesas livres": "#e7e43c",
    "investimentos": "#9b59b6",
}

LEGEND_CONFIG = dict(
    orientation="h",
    yanchor="top",
    y=-0.3,
    xanchor="center",
    x=0.5
)

LAYOUT_CONFIG = dict(
    height=420,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    showlegend=True,
    legend=LEGEND_CONFIG
)

def carregar_dados():
    return select(f"""
        SELECT
          a.is_self_employed as autonomo,
          b.due_day as dia_ref,
          b.amount as valor,
          CASE
            WHEN b.is_expense = FALSE THEN 'receitas'
            WHEN b.is_expense = TRUE AND b.is_essential_expense = TRUE THEN 'despesas essenciais'
            WHEN b.is_expense = TRUE AND b.is_free_expense = TRUE THEN 'despesas livres'
            WHEN b.is_expense = TRUE AND b.is_investment = TRUE THEN 'investimentos'
          END as categoria,
          b.description as descricao
        FROM users a
        LEFT JOIN transactions b ON a.id = b.user_id
        WHERE
          b.is_active = TRUE
          AND a.id = {st.session_state.user_id}
        ORDER BY b.due_day;
    """)

def calcular_totais(df):
    return {
        "receitas": df.loc[df["categoria"] == "receitas", "valor"].sum(),
        "essencial": df.loc[df["categoria"] == "despesas essenciais", "valor"].sum(),
        "livre": df.loc[df["categoria"] == "despesas livres", "valor"].sum(),
        "investimento": df.loc[df["categoria"] == "investimentos", "valor"].sum(),
    }

def preparar_dados_grafico(df):
    df_graph = df.groupby(["dia_ref", "categoria"], as_index=False).agg({"valor": "sum"})

    df_graph = df_graph.pivot(
        index="dia_ref",
        columns="categoria",
        values="valor"
    ).fillna(0).reset_index()

    df_graph = df_graph.rename(columns={"dia_ref": "dia"})

    df_graph["não atribuído"] = df_graph["receitas"] - (
        df_graph["despesas essenciais"] +
        df_graph["despesas livres"] +
        df_graph["investimentos"]
    )

    df_graph["dia"] = df_graph["dia"].astype(str)
    return df_graph

def criar_tooltip_itens(df):
    df_itens = df[["dia_ref", "categoria", "descricao", "valor"]].copy()
    df_itens["dia"] = df_itens["dia_ref"].astype(str)
    df_itens["tipo"] = df_itens["categoria"]

    df_tooltip = (
        df_itens.sort_values("valor", ascending=False)
        .groupby(["dia", "tipo"])
        .apply(lambda x: "<br>".join([
            f"R$ {row['valor']:.2f} - {row['descricao']}"
            for _, row in x.iterrows()
        ]))
        .reset_index(name="itens_html")
    )
    df_tooltip["key"] = df_tooltip["dia"] + "|" + df_tooltip["tipo"]
    return df_tooltip

def criar_hover_text(df_data, categoria, col_valor, df_tooltip=None):
    hover_list = []
    for _, row in df_data.iterrows():
        hover = f"<b>Categoria:</b> {categoria}<br><b>Valor total (R$):</b> {row[col_valor]:.2f}"
        if df_tooltip is not None and pd.notna(row.get("itens_html")):
            hover += f"<br><br>{row['itens_html']}"
        hover_list.append(hover)
    return hover_list

def adicionar_barra(fig, x, y, nome, cor, hover, width=0.15, offset=0):
    fig.add_trace(go.Bar(
        x=[i + offset for i in range(len(x))],
        y=y,
        name=nome,
        marker_color=cor,
        width=width,
        hovertemplate='%{customdata}<extra></extra>',
        customdata=hover,
        showlegend=True,
        legendgroup=nome
    ))

def criar_grafico_barras(df, df_graph):
    df_tooltip = criar_tooltip_itens(df)
    dias = df_graph["dia"].tolist()

    tem_nao_atribuido = (df_graph["não atribuído"] != 0).any()

    fig = go.Figure()

    num_barras = 5 if tem_nao_atribuido else 4
    espacamento = 0.15
    offset_inicial = -(num_barras - 1) * espacamento / 2

    df_receitas = df_graph[["dia", "receitas"]].copy()
    df_receitas["key"] = df_receitas["dia"] + "|receitas"
    df_receitas = df_receitas.merge(df_tooltip, on="key", how="left")

    adicionar_barra(
        fig,
        list(range(len(dias))),
        df_receitas["receitas"],
        "receitas",
        CORES["receitas"],
        criar_hover_text(df_receitas, "receitas", "receitas", df_tooltip),
        offset=offset_inicial
    )

    df_essencial = df_graph[["dia", "despesas essenciais"]].copy()
    df_essencial["key"] = df_essencial["dia"] + "|despesas essenciais"
    df_essencial = df_essencial.merge(df_tooltip, on="key", how="left")

    adicionar_barra(
        fig,
        list(range(len(dias))),
        df_essencial["despesas essenciais"],
        "despesas essenciais",
        CORES["despesas essenciais"],
        criar_hover_text(df_essencial, "despesas essenciais", "despesas essenciais", df_tooltip),
        offset=offset_inicial + espacamento
    )

    df_livres = df_graph[["dia", "despesas livres"]].copy()
    df_livres["key"] = df_livres["dia"] + "|despesas livres"
    df_livres = df_livres.merge(df_tooltip, on="key", how="left")

    adicionar_barra(
        fig,
        list(range(len(dias))),
        df_livres["despesas livres"],
        "despesas livres",
        CORES["despesas livres"],
        criar_hover_text(df_livres, "despesas livres", "despesas livres", df_tooltip),
        offset=offset_inicial + espacamento * 2
    )

    df_invest = df_graph[["dia", "investimentos"]].copy()
    df_invest["key"] = df_invest["dia"] + "|investimentos"
    df_invest = df_invest.merge(df_tooltip, on="key", how="left")

    adicionar_barra(
        fig,
        list(range(len(dias))),
        df_invest["investimentos"],
        "investimentos",
        CORES["investimentos"],
        criar_hover_text(df_invest, "investimentos", "investimentos", df_tooltip),
        offset=offset_inicial + espacamento * 3
    )

    if tem_nao_atribuido:
        adicionar_barra(
            fig,
            list(range(len(dias))),
            df_graph["não atribuído"],
            "não atribuído",
            CORES["não atribuído"],
            criar_hover_text(df_graph, "não atribuído", "não atribuído"),
            offset=offset_inicial + espacamento * 4
        )

    fig.update_layout(
        title={'text': "Movimentações por dia de referência", 'x': 0.5, 'xanchor': 'center'},
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(dias))),
            ticktext=dias
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False
        ),
        barmode='overlay',
        hovermode='closest',
        **LAYOUT_CONFIG
    )

    fig.update_xaxes(showgrid=False)

    return fig

def criar_grafico_pizza(totais):
    labels = ["despesas essenciais", "despesas livres", "investimentos"]
    values = [totais["essencial"], totais["livre"], totais["investimento"]]

    soma = sum(values)
    if soma < totais["receitas"]:
        labels.append("não atribuído")
        values.append(totais["receitas"] - soma)

    data = pd.DataFrame({"Categoria": labels, "Valor": values})
    data["Porcentagem"] = (data["Valor"] / totais["receitas"] * 100).round(1)

    hover_text = [
        f"<b>Categoria:</b> {cat}<br><b>Valor total (R$):</b> {val:,.2f}<br><b>Percentual:</b> {pct:.2f}%"
        for cat, val, pct in zip(data["Categoria"], data["Valor"], data["Porcentagem"])
    ]

    fig = go.Figure(data=[go.Pie(
        labels=data["Categoria"],
        values=data["Valor"],
        marker=dict(colors=[CORES[c] for c in data["Categoria"]]),
        hovertemplate='%{customdata}<extra></extra>',
        customdata=hover_text,
        textinfo='none'
    )])

    fig.update_layout(
        title={'text': "Distribuição das saídas em relação ao total de receitas", 'x': 0.5, 'xanchor': 'center'},
        **LAYOUT_CONFIG
    )

    return fig

def exibir_metricas(totais, autonomo):
    emergency_fund = totais["essencial"] * (12 if autonomo else 6)

    cols = st.columns(5, border=True)
    cols[0].metric("Receitas", f"R$ {totais['receitas']:.2f}")
    cols[1].metric("Gastos essenciais", f"R$ {totais['essencial']:.2f}")
    cols[2].metric("Gastos livres", f"R$ {totais['livre']:.2f}")
    cols[3].metric("Investimentos", f"R$ {totais['investimento']:.2f}")
    cols[4].metric(
        "Reserva de emergência",
        f"R$ {emergency_fund:.2f}",
        help="12 meses para autônomos, 6 meses para assalariados."
    )

try:
    st.subheader("Dashboard")

    df = carregar_dados()

    if df.empty:
        st.info("Nenhum dado encontrado.")
        st.stop()

    totais = calcular_totais(df)
    autonomo = bool(df["autonomo"].iloc[0])

    exibir_metricas(totais, autonomo)

    df_graph = preparar_dados_grafico(df)

    cols_graph = st.columns(2, border=True)

    with cols_graph[0]:
        st.plotly_chart(criar_grafico_barras(df, df_graph), use_container_width=True)

    with cols_graph[1]:
        st.plotly_chart(criar_grafico_pizza(totais), use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar página: {e}")