import streamlit as st
from pymongo import MongoClient

# Configuración de página
st.set_page_config(page_title="Matrículas CTP Rosario", layout="wide")

# Conexión a MongoDB
# Usamos tu URI directamente para evitar errores de configuración
uri = "mongodb+srv://haselaaa30:hola123@cluster1.d1jtuco.mongodb.net/?retryWrites=true&w=majority"
cliente = MongoClient(uri)
db = cliente["matriculas_2026"]
coleccion = db["estudiantes"]

st.title("🎓 Sistema de Matrículas - CTP Rosario de Naranjo")

# Mostrar datos en una tabla simple
st.subheader("Lista de Estudiantes Registrados")

try:
    estudiantes = list(coleccion.find())
    if estudiantes:
        # Esto crea una tabla automáticamente
        st.table(estudiantes)
    else:
        st.write("No hay estudiantes registrados todavía.")
except Exception as e:
    st.error(f"No se pudo conectar a la base de datos: {e}")
