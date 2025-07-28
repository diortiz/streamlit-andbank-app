import streamlit as st
import pandas as pd

st.set_page_config(page_title="Focus List - Fund Selection", layout="wide")

# --- Contraseña segura ---
PASSWORD = "andbank2025"

# --- Comprobación de contraseña usando sesión ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    with st.form("login_form", clear_on_submit=True):
        st.title("🔒 Acceso restringido")
        password = st.text_input("Introduce la contraseña:", type="password")
        login_button = st.form_submit_button("Entrar")

        if login_button:
            if password == PASSWORD:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta")
    st.stop()

st.title("Focus List - Fund Selection")


@st.cache_data
def cargar_datos():
    return pd.read_excel("prueba.xlsx")

df = cargar_datos()

# Convertir columnas numéricas
columnas_numericas = [
    "Rentabilidad semanal", "Rentabilidad mensual", "Rentabilidad 3 meses",
    "Rentabilidad YTD", "Rentabilidad 1 año", "Volatilidad 1 año",
    "Máxima caída 1 año", "Rentabilidad 2024", "Rentabilidad 3 años", "Rentabilidad 5 años",
    "Fund Size"
]

for col in columnas_numericas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Sidebar: selector de categoría
st.sidebar.title("Categorías")
st.sidebar.image("Andbankw.png", use_container_width = True)
categorias = ["Todas"] + sorted(df["Categoría"].dropna().unique())
categoria_seleccionada = st.sidebar.radio("Selecciona una categoría:", (categorias))

# Filtrado
if categoria_seleccionada != "Todas":
    df_filtrado = df[df["Categoría"] == categoria_seleccionada].copy()
else:
    df_filtrado = df.copy()

# Ordenar por Rentabilidad YTD descendente
if "Rentabilidad YTD" in df_filtrado.columns:
    df_filtrado = df_filtrado.sort_values("Rentabilidad YTD", ascending=False, na_position="last")

# Formatear columna "Fund Size"
def format_fund_size(valor, divisa):
    if pd.isna(valor) or valor == 0:
        return ""
    simbolo = "€" if divisa == "Euro" else "$" if divisa == "US Dollar" else ""
    return f"{valor:,.0f}".replace(",", ".") + f" {simbolo}"

df_filtrado["Fund Size"] = df_filtrado.apply(
    lambda row: format_fund_size(row["Fund Size"], row["Base Currency"]), axis=1
)

# Limpiar columna Currency Hedged
if "Currency Hedged" in df_filtrado.columns:
    df_filtrado["Currency Hedged"] = df_filtrado["Currency Hedged"].apply(
        lambda x: "" if pd.isna(x) or x == 0 else str(x)
    )

# Mostrar tabla
st.dataframe(df_filtrado, use_container_width=True)

# Pie de página
st.markdown(
    """
    <p style='text-align: right; font-style: italic; font-size: 0.9em; color: gray; margin-top: 10px;'>
    Fuente: Morningstar. Datos actualizados a cierre de semana.
    </p>
    """,
    unsafe_allow_html=True
)