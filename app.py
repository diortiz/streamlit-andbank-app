import streamlit as st
import pandas as pd

st.title("Focus List - Fund Selection")
st.write("Estas viendo el embrión de una nueva la nueva Focus List.")

def cargar_datos():
  return pd.read_excel("prueba.xlsx")

df = cargar_datos()

opciones = ["Todas"]+ sorted(df["Categoría"].dropna().unique().tolist())

seleccion = st.selectbox("Elige una categoría:",opciones)

if seleccion != "Todas":
  df_filtrado = df[df["Categoría"]== seleccion]

else:
  df_filtrado = df

st.subheader(f"Fondos en categoría: {seleccion}")
st.dataframe(df_filtrado)
