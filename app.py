from datetime import date
import streamlit as st
from pymongo import MongoClient

# Configuración de la página web
st.set_page_config(
    page_title="Sistema de Matrículas - CTP Rosario", layout="wide"
)

# Conexión a MongoDB Atlas (igual a la de tu programa de escritorio)
try:
  uri = "mongodb+srv://haselaaa30:hola123@cluster1.d1jtuco.mongodb.net/?retryWrites=true&w=majority"
  cliente = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
  cliente.admin.command("ping")
  col = cliente["matriculas_2026"]["estudiantes"]
except Exception as e:
  st.error(f"No se pudo conectar a MongoDB Atlas. Detalle: {e}")
  st.stop()

# Título Principal
st.title("🎓 Sistema de Matrículas - CTP Rosario de Naranjo")
st.markdown("---")

# Menú lateral (reemplaza los botones de tu panel izquierdo)
menu = st.sidebar.selectbox(
    "Navegación",
    [
        "Inicio",
        "Registrar Matrícula",
        "Ver Estudiantes",
        "Buscar Registro",
        "Eliminar Matrícula",
        "Estadísticas (Agregación)",
    ],
)

# --- MÓDULO 1: INICIO ---
if menu == "Inicio":
  st.subheader("Bienvenido al Sistema de Matrículas 2026")
  st.write(
      "Desarrollado para la subárea de Inteligencia Artificial.\nUse el panel"
      " de la izquierda para gestionar los registros en MongoDB Atlas."
  )

# --- MÓDULO 2: REGISTRAR MATRÍCULA ---
elif menu == "Registrar Matrícula":
  st.subheader("Formulario de Nueva Matrícula")

  with st.form("form_matricula"):
    nombre = st.text_input("Nombre completo *")
    cedula = st.text_input("Cédula *")
    especialidad = st.selectbox(
        "Especialidad *", [
            "Informática",
            "Contabilidad",
            "Secretariado",
            "Electrónica",
            "Agroindustria",
        ]
    )
    nivel = st.selectbox("Nivel *", ["Décimo", "Undécimo", "Duodécimo"])
    correo = st.text_input("Correo electrónico *")

    submitted = st.form_submit_button("Guardar Matrícula")

    if submitted:
      if not all([nombre, cedula, especialidad, nivel, correo]):
        st.warning("Por favor, complete todos los campos.")
      elif col.find_one({"cedula": cedula}):
        st.error("Esta cédula ya existe en la base de datos.")
      else:
        col.insert_one({
            "nombre": nombre,
            "cedula": cedula,
            "especialidad": especialidad,
            "nivel": nivel,
            "correo": correo,
            "activo": True,
            "fecha_reg": str(date.today()),
        })
        st.success(f"¡Estudiante {nombre} registrado con éxito!")

# --- MÓDULO 3: VER ESTUDIANTES ---
elif menu == "Ver Estudiantes":
  st.subheader("Lista de Estudiantes Matriculados")
  estudiantes = list(col.find({}))
  if estudiantes:
    datos_limpios = []
    for doc in estudiantes:
      datos_limpios.append({
          "Nombre": doc.get("nombre"),
          "Cédula": doc.get("cedula"),
          "Especialidad": doc.get("especialidad"),
          "Nivel": doc.get("nivel"),
          "Fecha": doc.get("fecha_reg"),
      })
    st.dataframe(datos_limpios, use_container_width=True)
  else:
    st.info("No hay estudiantes registrados todavía.")

# --- MÓDULO 4: BUSCAR REGISTRO ---
elif menu == "Buscar Registro":
  st.subheader("Buscador por Nombre")
  busqueda = st.text_input("Escriba el nombre a buscar:")
  if busqueda:
    resultados = list(
        col.find({"nombre": {"$regex": busqueda, "$options": "i"}})
    )
    if resultados:
      datos_busca = []
      for doc in resultados:
        datos_busca.append({
            "Nombre": doc.get("nombre"),
            "Cédula": doc.get("cedula"),
            "Especialidad": doc.get("especialidad"),
        })
      st.dataframe(datos_busca, use_container_width=True)
    else:
      st.warning("No se encontraron coincidencias.")

# --- MÓDULO 5: ELIMINAR MATRÍCULA ---
elif menu == "Eliminar Matrícula":
  st.subheader("Eliminar Matrícula")
  estudiantes = list(col.find({}))
  if estudiantes:
    opciones = {
        f"{doc.get('nombre')} (Cédula: {doc.get('cedula')})": doc["_id"]
        for doc in estudiantes
    }
    seleccion = st.selectbox(
        "Seleccione el estudiante a eliminar:", list(opciones.keys())
    )

    if st.button("Eliminar Seleccionado", type="primary"):
      id_a_borrar = opciones[seleccion]
      col.delete_one({"_id": id_a_borrar})
      st.success("Registro eliminado correctamente.")
      st.rerun()
  else:
    st.info("No hay registros para eliminar.")

# --- MÓDULO 6: ESTADÍSTICAS ---
elif menu == "Estadísticas (Agregación)":
  st.subheader("Métricas del Sistema (Aggregation Pipeline)")
  total = col.count_documents({})
  st.metric(label="Total de Matrículas Procesadas", value=total)

  res = list(
      col.aggregate([{"$group": {"_id": "$especialidad", "total": {"$sum": 1}}}])
  )
  st.write("### Distribución por Especialidad:")
  for r in res:
    st.write(f"• **{r['_id']}**: {r['total']} estudiantes")
