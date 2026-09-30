import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard de Ventas")
st.write("Análisis de ventas y rentabilidad")

df = pd.read_csv("base_ventas.csv")

df["Fecha"] = pd.to_datetime(df["Fecha"])

st.subheader("Vista de la base de datos")

st.dataframe(df)