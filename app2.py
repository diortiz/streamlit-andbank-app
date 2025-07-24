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

# Función para formatear valores: 2 decimales, vacío si 0 o NaN
def formatear_valor(x):
    if pd.isna(x) or x == 0:
        return ""
    else:
        return f"{x:.2f}"

# Formateo de 'Fund Size' según 'Base Currency'
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

# Formatear 'Currency Hedged': ocultar si es 0
def formatear_currency_hedged(x):
    return "" if pd.isna(x) or x == 0 else str(x)

# Aplicar formateos directos a columnas no numéricas
df_filtrado["Fund Size"] = df_filtrado.apply(formatear_fund_size, axis=1)
df_filtrado["Currency Hedged"] = df_filtrado["Currency Hedged"].apply(formatear_currency_hedged)

# Crear diccionario de formato solo para columnas numéricas
format_dict = {col: formatear_valor for col in columnas_a_formatear if col in df_filtrado.columns}

# -----------------------
# ESTILOS DE LA TABLA
# -----------------------

# Zebra alterna
def color_filas_alternas(x):
    return ['background-color: #f9f9f9' if i % 2 == 0 else 'background-color: white' for i in range(len(x))]

# Estilo del encabezado
header_styles = {
    'selector': 'th',
    'props': [
        ('background-color', '#003366'),
        ('color', 'white'),
        ('font-weight', 'bold'),
        ('text-align', 'center')
    ]
}

# Aplicar estilo
styled_df = (
    df_filtrado.style
    .apply(color_filas_alternas, axis=1)
    .format(format_dict)
    .set_properties(**{'text-align': 'left'})
    .set_table_styles([header_styles])
)

st.dataframe(styled_df, use_container_width=True)

# -----------------------
# FUENTE Y FECHA
# -----------------------
st.markdown(
    """
    <p style='text-align: right; font-style: italic; font-size: 0.9em; color: gray; margin-top: 10px;'>
    Fuente: Morningstar. Datos actualizados a cierre de semana.
    </p>
    """,
    unsafe_allow_html=True
)