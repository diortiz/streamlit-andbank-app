import streamlit as st

st.title("🌐 Web Vacía - Tema Andbank")
st.write("Esta es una plantilla mínima con el tema corporativo aplicado.")

opciones = ["Elige una categoría", "Renta Variable","Renta Fija"]

seleccion = st.selectbox("Elige una opción:",opciones)

if seleccion != "Elige una categoría":
  st.success(f"Has seleccionado: {seleccion}")

else:
  st.info("Por favor, selecciona una opción del menú.")
