import streamlit as st
from pymongo import MongoClient

# Conexión a MongoDB (la misma que tenías en tu código)
uri = "mongodb+srv://haselaaa30:hola123@cluster1.d1jtuco.mongodb.net/?retryWrites=true&w=majority"
cliente = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
col = cliente["matriculas_2026"]["estudiantes"]

st.set_page_config(page_title="Sistema de Matrículas", layout="wide")

st.title("🎓 Sistema de Matrículas - CTP Rosario de Naranjo")

# Menú lateral como el de tu app original
menu = st.sidebar.radio("Navegación", ["Inicio", "Registrar Matrícula", "Ver Estudiantes", "Estadísticas"])

if menu == "Inicio":
    st.write("Bienvenido al Sistema de Matrículas 2026.")
    st.info("Use el panel de la izquierda para gestionar los registros.")

elif menu == "Registrar Matrícula":
    st.subheader("Nueva Matrícula")
    nombre = st.text_input("Nombre completo")
    cedula = st.text_input("Cédula")
    especialidad = st.selectbox("Especialidad", ["Informática", "Contabilidad", "Secretariado", "Electrónica", "Agroindustria"])
    nivel = st.selectbox("Nivel", ["Décimo", "Undécimo", "Duodécimo"])
    correo = st.text_input("Correo electrónico")
    
    if st.button("Guardar Matrícula"):
        if nombre and cedula and correo:
            col.insert_one({"nombre": nombre, "cedula": cedula, "especialidad": especialidad, "nivel": nivel, "correo": correo})
            st.success("¡Estudiante registrado con éxito!")
        else:
            st.error("Por favor, complete todos los campos.")

elif menu == "Ver Estudiantes":
    st.subheader("Lista de Estudiantes")
    datos = list(col.find({}, {"_id": 0}))
    if datos:
        st.table(datos)
    else:
        st.write("No hay estudiantes registrados.")

elif menu == "Estadísticas":
    st.subheader("Métricas del Sistema")
    total = col.count_documents({})
    st.write(f"Total de Matrículas: {total}")
    res = list(col.aggregate([{"$group": {"_id": "$especialidad", "total": {"$sum": 1}}}]))
    for r in res:
        st.write(f"{r['_id']}: {r['total']} estudiantes")
