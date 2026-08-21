import streamlit as st
from pymongo import MongoClient

st.set_page_config(page_title="Matrículas CTP Rosario", layout="wide")

# Conexión a MongoDB Atlas
uri = "mongodb+srv://haselaaa30:hola123@cluster1.d1jtuco.mongodb.net/?retryWrites=true&w=majority"
cliente = MongoClient(uri)
db = cliente["matriculas_2026"]
coleccion = db["estudiantes"]

st.title("🎓 Sistema de Matrículas - CTP Rosario de Naranjo")
st.markdown("---")

st.subheader("Lista de Estudiantes Registrados")

try:
  estudiantes = list(coleccion.find())
  if estudiantes:
    datos_limpios = []
    for doc in estudiantes:
      datos_limpios.append({
          "Nombre": doc.get("nombre", "N/D"),
          "Cédula": doc.get("cedula", "N/D"),
          "Especialidad": doc.get("especialidad", "N/D"),
          "Nivel": doc.get("nivel", "N/D"),
          "Correo": doc.get("correo", "N/D"),
      })
    st.dataframe(datos_limpios, use_container_width=True)
  else:
    st.info("No hay estudiantes registrados todavía.")
except Exception as e:
  st.error(f"Error al conectar con la base de datos: {e}")
