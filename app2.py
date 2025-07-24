import streamlit as st
import pandas as pd

st.set_page_config(page_title="Focus List - Fund Selection", layout="wide")
st.title("Focus List - Fund Selection")


def cargar_datos():
    return pd.read_excel("prueba.xlsx")

df = cargar_datos()

# ---------------------
# FILTRO POR CATEGORÍA
# ---------------------
categorias = ["Todas"] + sorted(df["Categoría"].dropna().unique().tolist())
categoria_seleccionada = st.selectbox("Filtrar por categoría:", categorias)

if categoria_seleccionada != "Todas":
    df_filtrado = df[df["Categoría"] == categoria_seleccionada].copy()
else:
    df_filtrado = df.copy()

# ---------------------
# FORMATEO DE COLUMNAS
# ---------------------
columnas_formatear = [
    "Rentabilidad semanal", "Rentabilidad mensual", "Rentabilidad 3 meses",
    "Rentabilidad YTD", "Rentabilidad 1 año", "Volatilidad 1 año",
    "Máxima caída 1 año", "Rentabilidad 2024", "Rentabilidad 3 años", "Rentabilidad 5 años"
]

def formatear_valor(x):
    if pd.isna(x) or x == 0:
        return ""
    else:
        return f"{x:.2f}"

def formatear_fund_size(row):
    valor = row.get("Fund Size")
    divisa = row.get("Base Currency")

    if pd.isna(valor) or valor == 0:
        return ""

    try:
        valor_str = f"{int(valor):,}".replace(",", ".")
        simbolo = "€" if divisa == "Euro" else "$" if divisa == "US Dollar" else ""
        return f"{valor_str} {simbolo}"
    except:
        return ""

def formatear_currency_hedged(x):
    return "" if pd.isna(x) or x == 0 else str(x)

# Aplicar formatos
for col in columnas_formatear:
    if col in df_filtrado.columns:
        df_filtrado[col] = df_filtrado[col].apply(formatear_valor)

df_filtrado["Fund Size"] = df_filtrado.apply(formatear_fund_size, axis=1)
df_filtrado["Currency Hedged"] = df_filtrado["Currency Hedged"].apply(formatear_currency_hedged)

# ---------------------
# ORDENACIÓN DINÁMICA
# ---------------------
st.markdown("### 🔽 Ordenar tabla")
columna_orden = st.selectbox(
    "Seleccionar columna para ordenar:",
    options=["Rentabilidad YTD", "Rentabilidad 1 año", "Fund Size"]
)

orden_descendente = st.checkbox("Orden descendente", value=True)

# Convertir Fund Size a número para ordenación (crear columna oculta)
df_ordenar = df.copy()
df_ordenar["__Fund Size Num"] = pd.to_numeric(df_ordenar["Fund Size"], errors="coerce")

# Seleccionar columna real para ordenar
if columna_orden == "Fund Size":
    df_filtrado["__Fund Size Num"] = df_ordenar["__Fund Size Num"]
    df_filtrado = df_filtrado.sort_values("__Fund Size Num", ascending=not orden_descendente)
    df_filtrado = df_filtrado.drop(columns=["__Fund Size Num"])
else:
    df_filtrado = df_filtrado.sort_values(columna_orden, ascending=not orden_descendente)

# ---------------------
# MOSTRAR TABLA
# ---------------------
st.dataframe(df_filtrado, use_container_width=True)

# ---------------------
# PIE DE PÁGINA
# ---------------------
st.markdown(
    """
    <p style='text-align: right; font-style: italic; font-size: 0.9em; color: gray; margin-top: 10px;'>
    Fuente: Morningstar. Datos actualizados a cierre de semana.
    </p>
    """,
    unsafe_allow_html=True
)