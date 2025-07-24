import streamlit as st

st.title("🌐 Web con Menú Desplegable")

# Opciones del menú
opciones = ["Selecciona una opción", "Opción 1", "Opción 2", "Opción 3"]

# Desplegable
seleccion = st.selectbox("Elige una opción:", opciones)

# Resultado
if seleccion != "Selecciona una opción":
    st.success(f"Has seleccionado: {seleccion}")
else:
    st.info("Por favor, selecciona una opción del menú.")