# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 10:17:48 2026

@author: ESTUDIANTES
"""
""
from datetime import date
import tkinter as tk
from tkinter import messagebox, ttk
from bson.objectid import ObjectId
from pymongo import MongoClient


class AppMatriculas:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Matrículas - CTP Rosario de Naranjo")
        self.root.minsize(1050, 650)
        self.root.configure(bg="#f0f4fa")

        # Conexión a MongoDB Atlas
        try:
            # REEMPLAZA <db_password> con tu contraseña real (sin los símbolos < >)
            uri = "mongodb+srv://haselaaa30:hola123@cluster1.d1jtuco.mongodb.net/?retryWrites=true&w=majority"
            
            cliente = MongoClient(
                uri, 
                tls=True, 
                tlsAllowInvalidCertificates=True
            )
            cliente.admin.command("ping")

            # Base de datos y colección
            self.col = cliente["matriculas_2026"]["estudiantes"]

        except Exception as e:
            messagebox.showerror(
                "Error de Conexión",
                "No se pudo conectar a MongoDB Atlas.\n\n"
                f"Detalle del error: {e}",
            )
            self.root.destroy()
            return

        # Inicializar los componentes visuales de la aplicación
        self._crear_panel_nav()
        self.frame_cont = tk.Frame(self.root, bg="#f0f4fa")
        self.frame_cont.pack(side="right", fill="both", expand=True)
        self._mostrar_bienvenida()

    def _crear_panel_nav(self):
        """Panel lateral izquierdo para la navegación del CRUD"""
        nav = tk.Frame(self.root, bg="#1F3864", width=220)
        nav.pack(side="left", fill="y")
        nav.pack_propagate(False)

        tk.Label(
            nav,
            text="MATRÍCULAS\nCTP ROSARIO",
            bg="#1F3864",
            fg="white",
            font=("Arial", 12, "bold"),
            pady=20,
        ).pack(fill="x")

        modulos = [
            ("Inicio", self._mostrar_bienvenida),
            ("Registrar Matrícula", self._mod_registrar),
            ("Ver Estudiantes", self._mod_ver_todas),
            ("Buscar Registro", self._mod_buscar),
            ("Eliminar Matrícula", self._mod_eliminar),
            ("Estadísticas (Agregación)", self._mod_estadisticas),
        ]

        for texto, cmd in modulos:
            tk.Button(
                nav,
                text=texto,
                command=cmd,
                bg="#1F3864",
                fg="white",
                font=("Arial", 10),
                relief="flat",
                pady=12,
                anchor="w",
                padx=15,
                activebackground="#2E5090",
            ).pack(fill="x", pady=1)

    def _limpiar(self):
        """Limpia el contenedor central antes de cargar un nuevo módulo"""
        for w in self.frame_cont.winfo_children():
            w.destroy()

    def _mostrar_bienvenida(self):
        self._limpiar()
        tk.Label(
            self.frame_cont,
            text="Bienvenido al Sistema de Matrículas\nCTP Rosario de Naranjo 2026",
            font=("Arial", 22, "bold"),
            bg="#f0f4fa",
            fg="#1F3864",
            pady=60,
        ).pack()

        tk.Label(
            self.frame_cont,
            text=(
                "Desarrollado para la subárea de Inteligencia Artificial.\n"
                "Use el panel de la izquierda para gestionar los registros en MongoDB Atlas."
            ),
            font=("Arial", 11, "italic"),
            bg="#f0f4fa",
            fg="#555555",
        ).pack()

    def _mod_registrar(self):
        self._limpiar()
        tk.Label(
            self.frame_cont,
            text="Formulario de Nueva Matrícula",
            font=("Arial", 16, "bold"),
            bg="#f0f4fa",
            fg="#1F3864"
        ).pack(pady=15)
        
        f = tk.Frame(self.frame_cont, bg="#f0f4fa")
        f.pack(pady=10)

        tk.Label(f, text="Nombre completo *:", bg="#f0f4fa").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.e_nombre = tk.Entry(f, width=40)
        self.e_nombre.grid(row=0, column=1, pady=5)

        tk.Label(f, text="Cédula *:", bg="#f0f4fa").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.e_cedula = tk.Entry(f, width=40)
        self.e_cedula.grid(row=1, column=1, pady=5)

        tk.Label(f, text="Especialidad *:", bg="#f0f4fa").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.cb_espec = ttk.Combobox(f, values=["Informática", "Contabilidad", "Secretariado", "Electrónica", "Agroindustria"], width=37, state="readonly")
        self.cb_espec.grid(row=2, column=1, pady=5)

        tk.Label(f, text="Nivel *:", bg="#f0f4fa").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        self.cb_nivel = ttk.Combobox(f, values=["Décimo", "Undécimo", "Duodécimo"], width=37, state="readonly")
        self.cb_nivel.grid(row=3, column=1, pady=5)

        tk.Label(f, text="Correo electrónico *:", bg="#f0f4fa").grid(row=4, column=0, sticky="w", pady=5, padx=5)
        self.e_correo = tk.Entry(f, width=40)
        self.e_correo.grid(row=4, column=1, pady=5)

        tk.Button(
            self.frame_cont,
            text="Guardar Matrícula",
            command=self._guardar_matricula,
            bg="#2E7D32",
            fg="white",
            font=("Arial", 10, "bold"),
            width=25,
            pady=6
        ).pack(pady=25)

    def _guardar_matricula(self):
        n, c, e, ni, co = self.e_nombre.get().strip(), self.e_cedula.get().strip(), self.cb_espec.get(), self.cb_nivel.get(), self.e_correo.get().strip()
        if not all([n, c, e, ni, co]):
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
            return
        if self.col.find_one({"cedula": c}):
            messagebox.showerror("Error", "Esta cédula ya existe.")
            return
        self.col.insert_one({"nombre": n, "cedula": c, "especialidad": e, "nivel": ni, "correo": co, "activo": True, "fecha_reg": str(date.today())})
        messagebox.showinfo("Éxito", f"¡Estudiante {n} registrado!")
        self._mod_registrar()

    def _mod_ver_todas(self):
        self._limpiar()
        
        tk.Label(
            self.frame_cont,
            text="Lista de Estudiantes Matriculados",
            font=("Arial", 16, "bold"),
            bg="#f0f4fa",
            fg="#1F3864"
        ).pack(pady=15)

        tree = ttk.Treeview(self.frame_cont, columns=("Nombre", "Cédula", "Especialidad", "Nivel", "Fecha"), show="headings")
        for col in ("Nombre", "Cédula", "Especialidad", "Nivel", "Fecha"):
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        for doc in self.col.find({}):
            tree.insert("", "end", iid=str(doc["_id"]), values=(doc.get("nombre"), doc.get("cedula"), doc.get("especialidad"), doc.get("nivel"), doc.get("fecha_reg")))
        
        tk.Button(self.frame_cont, text="Recargar Lista", command=self._mod_ver_todas, bg="#1F3864", fg="white").pack(pady=10)

    def _mod_buscar(self):
        self._limpiar()
        
        tk.Label(
            self.frame_cont,
            text="Buscador por Nombre",
            font=("Arial", 16, "bold"),
            bg="#f0f4fa",
            fg="#1F3864"
        ).pack(pady=15)

        f = tk.Frame(self.frame_cont, bg="#f0f4fa")
        f.pack(pady=10)
        
        tk.Label(f, text="Nombre:", bg="#f0f4fa").pack(side="left", padx=5)
        entry = tk.Entry(f, width=30)
        entry.pack(side="left", padx=5)
        
        tree = ttk.Treeview(self.frame_cont, columns=("Nombre", "Cédula", "Especialidad"), show="headings")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Cédula", text="Cédula")
        tree.heading("Especialidad", text="Especialidad")
        for col in ("Nombre", "Cédula", "Especialidad"):
            tree.column(col, anchor="center")
            
        tree.pack(fill="both", expand=True, padx=20, pady=10)

        def buscar():
            for r in tree.get_children(): 
                tree.delete(r)
            for doc in self.col.find({"nombre": {"$regex": entry.get(), "$options": "i"}}):
                tree.insert("", "end", values=(doc.get("nombre"), doc.get("cedula"), doc.get("especialidad")))
        
        tk.Button(f, text="Buscar", command=buscar, bg="#1F3864", fg="white").pack(side="left", padx=5)

    def _mod_eliminar(self):
        self._limpiar()
        
        tk.Label(
            self.frame_cont,
            text="Eliminar Matrícula",
            font=("Arial", 16, "bold"),
            bg="#f0f4fa",
            fg="#1F3864"
        ).pack(pady=15)

        tree = ttk.Treeview(self.frame_cont, columns=("Nombre", "Cédula"), show="headings")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Cédula", text="Cédula")
        tree.column("Nombre", anchor="center")
        tree.column("Cédula", anchor="center")
        tree.pack(fill="x", padx=20, pady=10)
        
        for doc in self.col.find({}): 
            tree.insert("", "end", iid=str(doc["_id"]), values=(doc.get("nombre"), doc.get("cedula")))
        
        def borrar():
            sel = tree.focus()
            if sel and messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?"):
                self.col.delete_one({"_id": ObjectId(sel)})
                messagebox.showinfo("Éxito", "Registro eliminado.")
                self._mod_eliminar()
            elif not sel:
                messagebox.showwarning("Selección vacía", "Seleccione un estudiante de la tabla.")
        
        tk.Button(self.frame_cont, text="Eliminar Seleccionado", command=borrar, bg="#C62828", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

    def _mod_estadisticas(self):
        self._limpiar()
        
        tk.Label(
            self.frame_cont,
            text="Métricas del Sistema (Aggregation Pipeline)",
            font=("Arial", 16, "bold"),
            bg="#f0f4fa",
            fg="#1F3864"
        ).pack(pady=15)

        total = self.col.count_documents({})
        res = list(self.col.aggregate([{"$group": {"_id": "$especialidad", "total": {"$sum": 1}}}]))
        
        texto = f"Total de Matrículas Procesadas: {total}\n\nDistribución por Especialidad:\n"
        for r in res:
            texto += f"  • {r['_id']}: {r['total']} estudiantes\n"
            
        tk.Label(self.frame_cont, text=texto, font=("Consolas", 12), bg="white", justify="left", padx=25, pady=25, relief="solid", bd=1).pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = AppMatriculas(root)
    root.mainloop()