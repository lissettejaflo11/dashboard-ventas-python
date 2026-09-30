import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# CARGAR BASE DE DATOS
# --------------------------------------------------

df = pd.read_csv("base_ventas.csv")

df["Fecha"] = pd.to_datetime(df["Fecha"])

# --------------------------------------------------
# TÍTULO
# --------------------------------------------------

st.title("📊 Dashboard de Ventas y Rentabilidad")
st.markdown(
    "Análisis comercial desarrollado con Python, Pandas y Streamlit"
)

# --------------------------------------------------
# SIDEBAR - FILTROS
# --------------------------------------------------

st.sidebar.header("🔎 Filtros")

regiones = st.sidebar.multiselect(
    "Región",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categorias = st.sidebar.multiselect(
    "Categoría",
    options=sorted(df["Categoria"].unique()),
    default=sorted(df["Categoria"].unique())
)

canales = st.sidebar.multiselect(
    "Canal",
    options=sorted(df["Canal"].unique()),
    default=sorted(df["Canal"].unique())
)

fecha_min = df["Fecha"].min()
fecha_max = df["Fecha"].max()

fecha_inicio = st.sidebar.date_input(
    "Fecha inicial",
    fecha_min
)

fecha_fin = st.sidebar.date_input(
    "Fecha final",
    fecha_max
)

# --------------------------------------------------
# APLICAR FILTROS
# --------------------------------------------------

df_filtrado = df[
    (df["Region"].isin(regiones)) &
    (df["Categoria"].isin(categorias)) &
    (df["Canal"].isin(canales)) &
    (df["Fecha"].dt.date >= fecha_inicio) &
    (df["Fecha"].dt.date <= fecha_fin)
].copy()

# --------------------------------------------------
# MENSAJE SI NO HAY DATOS
# --------------------------------------------------

if df_filtrado.empty:

    st.warning(
        "No existen datos para los filtros seleccionados."
    )

    st.stop()

# --------------------------------------------------
# KPIs
# --------------------------------------------------

ventas_totales = df_filtrado["Venta_Total"].sum()
ganancia_total = df_filtrado["Ganancia"].sum()
numero_ventas = len(df_filtrado)
margen_promedio = df_filtrado["Margen_Porcentaje"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Ventas Totales",
    f"S/ {ventas_totales:,.2f}"
)

col2.metric(
    "📈 Ganancia Total",
    f"S/ {ganancia_total:,.2f}"
)

col3.metric(
    "🛒 Número de Ventas",
    f"{numero_ventas:,}"
)

col4.metric(
    "📊 Margen Promedio",
    f"{margen_promedio:.2f}%"
)

st.divider()

# --------------------------------------------------
# PREPARAR DATOS MENSUALES
# --------------------------------------------------

df_filtrado["Mes"] = df_filtrado["Fecha"].dt.to_period("M").astype(str)

ventas_mensuales = (
    df_filtrado
    .groupby("Mes", as_index=False)["Venta_Total"]
    .sum()
)

# --------------------------------------------------
# VENTAS POR CATEGORÍA
# --------------------------------------------------

ventas_categoria = (
    df_filtrado
    .groupby("Categoria", as_index=False)
    .agg(
        Ventas=("Venta_Total", "sum"),
        Ganancia=("Ganancia", "sum")
    )
)

# --------------------------------------------------
# VENTAS POR CANAL
# --------------------------------------------------

ventas_canal = (
    df_filtrado
    .groupby("Canal", as_index=False)["Venta_Total"]
    .sum()
)

# --------------------------------------------------
# MARGEN POR REGIÓN
# --------------------------------------------------

margen_region = (
    df_filtrado
    .groupby("Region", as_index=False)["Margen_Porcentaje"]
    .mean()
)

# --------------------------------------------------
# GRÁFICOS
# --------------------------------------------------

col1, col2 = st.columns(2)

# Gráfico 1
fig_mensual = px.line(
    ventas_mensuales,
    x="Mes",
    y="Venta_Total",
    markers=True,
    title="📈 Evolución Mensual de Ventas",
    labels={
        "Mes": "Mes",
        "Venta_Total": "Ventas (S/.)"
    }
)

fig_mensual.update_layout(
    hovermode="x unified"
)

col1.plotly_chart(
    fig_mensual,
    use_container_width=True
)

# Gráfico 2
fig_categoria = px.bar(
    ventas_categoria.sort_values("Ganancia"),
    x="Ganancia",
    y="Categoria",
    orientation="h",
    title="💵 Ganancia por Categoría",
    labels={
        "Ganancia": "Ganancia (S/.)",
        "Categoria": "Categoría"
    },
    text_auto=".2s"
)

col2.plotly_chart(
    fig_categoria,
    use_container_width=True
)

# --------------------------------------------------
# SEGUNDA FILA
# --------------------------------------------------

col3, col4 = st.columns(2)

# Gráfico 3
fig_canal = px.pie(
    ventas_canal,
    names="Canal",
    values="Venta_Total",
    hole=0.4,
    title="🛒 Participación de Ventas por Canal"
)

col3.plotly_chart(
    fig_canal,
    use_container_width=True
)

# Gráfico 4
fig_region = px.bar(
    margen_region,
    x="Region",
    y="Margen_Porcentaje",
    title="🌎 Margen Promedio por Región",
    labels={
        "Region": "Región",
        "Margen_Porcentaje": "Margen (%)"
    },
    text_auto=".1f"
)

fig_region.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

col4.plotly_chart(
    fig_region,
    use_container_width=True
)

# --------------------------------------------------
# TABLA DE DATOS
# --------------------------------------------------

st.divider()

st.subheader("📋 Detalle de las ventas")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

# --------------------------------------------------
# PIE DE PÁGINA
# --------------------------------------------------

st.divider()

st.caption(
    "Proyecto final de Python Avanzado | Dashboard de Ventas y Rentabilidad"
)
