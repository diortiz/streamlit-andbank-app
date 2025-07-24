import streamlit as st
import pandas as pd

# Función simple para pedir contraseña
def pedir_password():
    st.sidebar.title("Acceso restringido")
    password = st.sidebar.text_input("Introduce la contraseña:", type="password")
    return password

# Define aquí tu contraseña segura
PASSWORD = "andbank123"  # cambia esto por la contraseña que quieras

password_introducida = pedir_password()

if password_introducida != PASSWORD:
    st.error("🔒 Contraseña incorrecta. Acceso denegado.")
    st.stop()  # detiene la ejecución si la contraseña es errónea

st.set_page_config(page_title="Focus List - Fund Selection", layout="wide")
st.title("Focus List - Fund Selection")


def cargar_datos():
    return pd.read_excel("prueba.xlsx")

df = cargar_datos()

# Filtrar por categoría
categorias = ["Todas"] + sorted(df["Categoría"].dropna().unique())
categoria_seleccionada = st.selectbox("Filtrar por categoría:", categorias)

if categoria_seleccionada != "Todas":
    df_filtrado = df[df["Categoría"] == categoria_seleccionada].copy()
else:
    df_filtrado = df.copy()

# Convertir columnas numéricas para asegurar orden correcto
columnas_numericas = [
    "Rentabilidad semanal", "Rentabilidad mensual", "Rentabilidad 3 meses",
    "Rentabilidad YTD", "Rentabilidad 1 año", "Volatilidad 1 año",
    "Máxima caída 1 año", "Rentabilidad 2024", "Rentabilidad 3 años", "Rentabilidad 5 años",
    "Fund Size"
]

for col in columnas_numericas:
    if col in df_filtrado.columns:
        df_filtrado[col] = pd.to_numeric(df_filtrado[col], errors='coerce')

# Orden fijo por Rentabilidad YTD descendente
if "Rentabilidad YTD" in df_filtrado.columns:
    df_filtrado = df_filtrado.sort_values("Rentabilidad YTD", ascending=False, na_position='last')

# Formatear Fund Size como string para mostrar con separadores y símbolo
def format_fund_size(valor, divisa):
    if pd.isna(valor) or valor == 0:
        return ""
    simbolo = "€" if divisa == "Euro" else "$" if divisa == "US Dollar" else ""
    return f"{valor:,.0f}".replace(",", ".") + f" {simbolo}"

df_filtrado["Fund Size"] = df_filtrado.apply(
    lambda row: format_fund_size(row["Fund Size"], row["Base Currency"]) if ("Fund Size" in df_filtrado.columns and "Base Currency" in df_filtrado.columns) else "", axis=1
)

# Mostrar tabla directamente sin formato visual en columnas numéricas
st.dataframe(df_filtrado, use_container_width=True)

st.markdown(
    """
    <p style='text-align: right; font-style: italic; font-size: 0.9em; color: gray; margin-top: 10px;'>
    Fuente: Morningstar. Datos actualizados a cierre de semana.
    </p>
    """,
    unsafe_allow_html=True
)