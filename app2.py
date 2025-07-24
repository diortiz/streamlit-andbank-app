import streamlit as st
import pandas as pd

st.set_page_config(page_title="Focus List - Fund Selection", layout="wide")
st.title("Focus List - Fund Selection")


def cargar_datos():
    return pd.read_excel("prueba.xlsx")

df = cargar_datos()

categorias = ["Todas"] + sorted(df["Categoría"].dropna().unique().tolist())
categoria_seleccionada = st.selectbox("Filtrar por categoría:", categorias)

if categoria_seleccionada != "Todas":
    df_filtrado = df[df["Categoría"] == categoria_seleccionada]
else:
    df_filtrado = df

# Lista de columnas numéricas que quieres formatear
columnas_a_formatear = [
    "Rentabilidad semanal",
    "Rentabilidad mensual",
    "Rentabilidad 3 meses",
    "Rentabilidad YTD",
    "Rentabilidad 1 año",
    "Volatilidad 1 año",
    "Máxima caída 1 año",
    "Rentabilidad 2024",
    "Rentabilidad 3 años",
    "Rentabilidad 5 años"
]  # ajusta según tus columnas

# Crear función para aplicar color alterno (zebra)
def color_filas_alternas(x):
    return ['background-color: #f9f9f9' if i % 2 == 0 else 'background-color: white' for i in range(len(x))]

# Aplicar estilos: formato decimal + filas zebra
styled_df = (
    df_filtrado.style
    .apply(color_filas_alternas, axis=1)
    .format({col: "{:.2f}" for col in columnas_a_formatear if col in df_filtrado.columns})
    .set_properties(**{'text-align': 'left'})
)

st.dataframe(styled_df, use_container_width=True)

st.markdown(
    """
    <p style='text-align: right; font-style: italic; font-size: 0.9em; color: gray; margin-top: 10px;'>
    Fuente: Morningstar. Datos actualizados a cierre de semana.
    </p>
    """,
    unsafe_allow_html=True
)