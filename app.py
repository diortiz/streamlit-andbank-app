import streamlit as st

st.title("Focus List - Fund Selection")
st.write("Estas viendo el embrión de una nueva la nueva Focus List.")

opciones = ["Elige una categoría", "Renta Variable","Renta Fija"]

seleccion = st.selectbox("Elige una opción:",opciones)

if seleccion != "Elige una categoría":
  st.success(f"Has seleccionado: {seleccion}")

else:
  st.info("Por favor, selecciona una opción del menú.")
