"""
Módulo 3: Módulo de Exposiciones
Creación de exposiciones, agrupando obras por tema o artista
Actor: Administrador
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from database import get_db
from bson.objectid import ObjectId
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import configure_styles, COLORS, FONTS

class ExposicionesWindow:
    def __init__(self):
        """Inicializa la ventana de gestión de exposiciones"""
        self.window = tk.Toplevel()
        self.window.title("Módulo de Exposiciones")
        self.window.geometry("1300x750")
        self.window.configure(bg=COLORS['bg_primary'])

        # Configurar estilos
        configure_styles()

        self.db = get_db()
        self.exposiciones_collection = self.db.get_collection('exposiciones')
        self.obras_collection = self.db.get_collection('obras')
        self.artistas_collection = self.db.get_collection('artistas')

        self.selected_exposicion_id = None
        self.obras_seleccionadas = []

        self.setup_ui()
        self.load_exposiciones()
        self.load_obras_disponibles()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Header
        header_frame = tk.Frame(self.window, bg='#E67E22', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Título en el header
        title_label = tk.Label(
            header_frame,
            text="🏛️ EXPOSICIONES",
            font=('Segoe UI', 20, 'bold'),
            bg='#E67E22',
            fg=COLORS['text_light']
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=30)

        subtitle_label = tk.Label(
            header_frame,
            text="Gestión de exposiciones agrupando obras por tema o artista",
            font=('Segoe UI', 10),
            bg='#E67E22',
            fg=COLORS['text_light']
        )
        subtitle_label.pack(side=tk.LEFT, padx=(0, 30), pady=30)

        # Frame principal
        main_frame = tk.Frame(self.window, bg=COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel izquierdo - Lista de exposiciones
        left_panel = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Título del panel izquierdo
        left_title_frame = tk.Frame(left_panel, bg=COLORS['bg_secondary'], height=50)
        left_title_frame.pack(fill=tk.X, pady=(0, 5))
        left_title_frame.pack_propagate(False)

        tk.Label(
            left_title_frame,
            text="Lista de Exposiciones",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).pack(side=tk.LEFT, padx=15, pady=10)

        # Treeview con estilo
        tree_frame = tk.Frame(left_panel, bg=COLORS['bg_secondary'], relief='solid', borderwidth=1)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview
        columns = ("nombre", "tema", "fecha_inicio", "fecha_fin", "num_obras")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings", height=20)

        self.tree.heading("#0", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("tema", text="Tema")
        self.tree.heading("fecha_inicio", text="F. Inicio")
        self.tree.heading("fecha_fin", text="F. Fin")
        self.tree.heading("num_obras", text="Obras")

        self.tree.column("#0", width=40)
        self.tree.column("nombre", width=150)
        self.tree.column("tema", width=120)
        self.tree.column("fecha_inicio", width=100)
        self.tree.column("fecha_fin", width=100)
        self.tree.column("num_obras", width=60)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<<TreeviewSelect>>', self.on_select_exposicion)

        # Panel derecho - Formulario
        right_panel = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Título del panel derecho
        right_title_frame = tk.Frame(right_panel, bg=COLORS['bg_secondary'], height=50)
        right_title_frame.pack(fill=tk.X, pady=(0, 5))
        right_title_frame.pack_propagate(False)

        tk.Label(
            right_title_frame,
            text="Datos de la Exposición",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).pack(side=tk.LEFT, padx=15, pady=10)

        # Formulario con fondo
        form_frame = tk.Frame(right_panel, bg=COLORS['bg_secondary'], relief='solid', borderwidth=1)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Contenedor con padding
        form_content = tk.Frame(form_frame, bg=COLORS['bg_secondary'])
        form_content.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        row = 0

        # Nombre
        tk.Label(
            form_content,
            text="Nombre:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(10, 5))

        self.nombre_entry = tk.Entry(
            form_content,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.nombre_entry.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15), ipady=8)
        row += 2

        # Tema
        tk.Label(
            form_content,
            text="Tema:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        self.tema_entry = tk.Entry(
            form_content,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.tema_entry.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15), ipady=8)
        row += 2

        # Fecha inicio
        tk.Label(
            form_content,
            text="Fecha Inicio:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        fecha_inicio_frame = tk.Frame(form_content, bg=COLORS['bg_secondary'])
        fecha_inicio_frame.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15))

        tk.Label(fecha_inicio_frame, text="Día:", bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT)
        self.dia_inicio_entry = tk.Entry(fecha_inicio_frame, width=5, font=('Segoe UI', 10))
        self.dia_inicio_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(fecha_inicio_frame, text="Mes:", bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT, padx=(10, 0))
        self.mes_inicio_entry = tk.Entry(fecha_inicio_frame, width=5, font=('Segoe UI', 10))
        self.mes_inicio_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(fecha_inicio_frame, text="Año:", bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT, padx=(10, 0))
        self.anio_inicio_entry = tk.Entry(fecha_inicio_frame, width=8, font=('Segoe UI', 10))
        self.anio_inicio_entry.pack(side=tk.LEFT, padx=2)
        row += 2

        # Fecha fin
        tk.Label(
            form_content,
            text="Fecha Fin:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        fecha_fin_frame = tk.Frame(form_content, bg=COLORS['bg_secondary'])
        fecha_fin_frame.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15))

        tk.Label(fecha_fin_frame, text="Día:", bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT)
        self.dia_fin_entry = tk.Entry(fecha_fin_frame, width=5, font=('Segoe UI', 10))
        self.dia_fin_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(fecha_fin_frame, text="Mes:", bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT, padx=(10, 0))
        self.mes_fin_entry = tk.Entry(fecha_fin_frame, width=5, font=('Segoe UI', 10))
        self.mes_fin_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(fecha_fin_frame, text="Año:", bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT, padx=(10, 0))
        self.anio_fin_entry = tk.Entry(fecha_fin_frame, width=8, font=('Segoe UI', 10))
        self.anio_fin_entry.pack(side=tk.LEFT, padx=2)
        row += 2

        # Descripción
        tk.Label(
            form_content,
            text="Descripción:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        self.descripcion_text = scrolledtext.ScrolledText(
            form_content,
            width=40,
            height=4,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1
        )
        self.descripcion_text.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15))
        row += 2

        # Separador
        separator = tk.Frame(form_content, bg=COLORS['border'], height=2)
        separator.grid(row=row, column=0, sticky=tk.EW, pady=10)
        row += 1

        # Obras de la exposición
        tk.Label(
            form_content,
            text="Obras de la Exposición:",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(0, 10))
        row += 1

        # Frame con las dos listboxes
        obras_container = tk.Frame(form_content, bg=COLORS['bg_secondary'])
        obras_container.grid(row=row, column=0, sticky=tk.NSEW, pady=(0, 15))

        # Disponibles
        disponibles_frame = tk.Frame(obras_container, bg=COLORS['bg_secondary'])
        disponibles_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(disponibles_frame, text="Disponibles", bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], font=('Segoe UI', 9, 'bold')).pack()
        self.obras_listbox = tk.Listbox(disponibles_frame, selectmode=tk.MULTIPLE, height=6, font=('Segoe UI', 9))
        self.obras_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        # Botones agregar/quitar
        buttons_obras_frame = tk.Frame(obras_container, bg=COLORS['bg_secondary'])
        buttons_obras_frame.pack(side=tk.LEFT, padx=10)

        tk.Button(buttons_obras_frame, text=">>", command=self.agregar_obras, width=5, bg=COLORS['accent'], fg=COLORS['text_light'], relief='flat').pack(pady=5)
        tk.Button(buttons_obras_frame, text="<<", command=self.quitar_obras, width=5, bg=COLORS['warning'], fg=COLORS['text_light'], relief='flat').pack(pady=5)

        # Seleccionadas
        seleccionadas_frame = tk.Frame(obras_container, bg=COLORS['bg_secondary'])
        seleccionadas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(seleccionadas_frame, text="Seleccionadas", bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], font=('Segoe UI', 9, 'bold')).pack()
        self.obras_selec_listbox = tk.Listbox(seleccionadas_frame, selectmode=tk.MULTIPLE, height=6, font=('Segoe UI', 9))
        self.obras_selec_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        row += 1

        # Configurar expansión
        form_content.columnconfigure(0, weight=1)
        form_content.rowconfigure(row-1, weight=1)

        # Botones de acción
        buttons_frame = tk.Frame(form_content, bg=COLORS['bg_secondary'])
        buttons_frame.grid(row=row, column=0, sticky=tk.EW, pady=(10, 0))

        # Crear botones con estilos
        btn_config = [
            ("Nueva", self.nueva_exposicion, COLORS['accent']),
            ("Guardar", self.guardar_exposicion, COLORS['success']),
            ("Actualizar", self.actualizar_exposicion, COLORS['warning']),
            ("Eliminar", self.eliminar_exposicion, COLORS['danger']),
            ("Limpiar", self.limpiar_formulario, COLORS['text_secondary'])
        ]

        for idx, (text, command, color) in enumerate(btn_config):
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=('Segoe UI', 10, 'bold'),
                bg=color,
                fg=COLORS['text_light'],
                activebackground=color,
                activeforeground=COLORS['text_light'],
                relief='flat',
                cursor='hand2',
                command=command
            )
            btn.grid(row=0, column=idx, padx=3, pady=5, sticky=tk.EW, ipady=8)
            buttons_frame.columnconfigure(idx, weight=1)

            # Efecto hover
            def make_hover(button, base_color):
                def on_enter(e):
                    button['bg'] = self.lighten_color(base_color)
                def on_leave(e):
                    button['bg'] = base_color
                button.bind("<Enter>", on_enter)
                button.bind("<Leave>", on_leave)

            make_hover(btn, color)

    def lighten_color(self, color):
        """Aclara un color hexadecimal"""
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'

    def load_obras_disponibles(self):
        """Carga las obras disponibles en el listbox"""
        self.obras_listbox.delete(0, tk.END)
        self.obras_dict = {}

        obras = self.obras_collection.find().sort("titulo", 1)

        for obra in obras:
            obra_id = str(obra['_id'])
            titulo = obra.get('titulo', 'Sin título')

            # Obtener nombre del artista
            artista_nombre = "Desconocido"
            if 'artista_id' in obra:
                artista = self.artistas_collection.find_one({'_id': ObjectId(obra['artista_id'])})
                if artista:
                    artista_nombre = artista['nombre']

            display_text = f"{titulo} - {artista_nombre}"
            self.obras_dict[display_text] = obra_id

            # Solo agregar si no está en la lista de seleccionadas
            if obra_id not in self.obras_seleccionadas:
                self.obras_listbox.insert(tk.END, display_text)

    def agregar_obras(self):
        """Agrega obras seleccionadas a la exposición"""
        seleccion = self.obras_listbox.curselection()

        for idx in reversed(seleccion):
            obra_text = self.obras_listbox.get(idx)
            obra_id = self.obras_dict[obra_text]

            if obra_id not in self.obras_seleccionadas:
                self.obras_seleccionadas.append(obra_id)
                self.obras_selec_listbox.insert(tk.END, obra_text)
                self.obras_listbox.delete(idx)

    def quitar_obras(self):
        """Quita obras de la exposición"""
        seleccion = self.obras_selec_listbox.curselection()

        for idx in reversed(seleccion):
            obra_text = self.obras_selec_listbox.get(idx)
            obra_id = self.obras_dict[obra_text]

            if obra_id in self.obras_seleccionadas:
                self.obras_seleccionadas.remove(obra_id)
                self.obras_selec_listbox.delete(idx)
                self.obras_listbox.insert(tk.END, obra_text)

    def load_exposiciones(self):
        """Carga todas las exposiciones en el TreeView"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        exposiciones = self.exposiciones_collection.find().sort("nombre", 1)

        for idx, expo in enumerate(exposiciones, 1):
            fecha_inicio = "N/A"
            fecha_fin = "N/A"

            if 'fecha_inicio' in expo and expo['fecha_inicio']:
                if isinstance(expo['fecha_inicio'], datetime):
                    fecha_inicio = expo['fecha_inicio'].strftime("%d/%m/%Y")

            if 'fecha_fin' in expo and expo['fecha_fin']:
                if isinstance(expo['fecha_fin'], datetime):
                    fecha_fin = expo['fecha_fin'].strftime("%d/%m/%Y")

            num_obras = len(expo.get('obras', []))

            self.tree.insert("", tk.END, iid=str(expo['_id']), text=str(idx),
                           values=(expo.get('nombre', ''),
                                 expo.get('tema', ''),
                                 fecha_inicio,
                                 fecha_fin,
                                 num_obras))

    def on_select_exposicion(self, event):
        """Maneja la selección de una exposición en el TreeView"""
        selection = self.tree.selection()
        if selection:
            exposicion_id = selection[0]
            self.selected_exposicion_id = exposicion_id
            self.load_exposicion_data(exposicion_id)

    def load_exposicion_data(self, exposicion_id):
        """Carga los datos de una exposición en el formulario"""
        exposicion = self.exposiciones_collection.find_one({'_id': ObjectId(exposicion_id)})

        if exposicion:
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, exposicion.get('nombre', ''))

            self.tema_entry.delete(0, tk.END)
            self.tema_entry.insert(0, exposicion.get('tema', ''))

            # Fechas
            if 'fecha_inicio' in exposicion and exposicion['fecha_inicio']:
                fecha = exposicion['fecha_inicio']
                if isinstance(fecha, datetime):
                    self.dia_inicio_entry.delete(0, tk.END)
                    self.dia_inicio_entry.insert(0, fecha.day)
                    self.mes_inicio_entry.delete(0, tk.END)
                    self.mes_inicio_entry.insert(0, fecha.month)
                    self.anio_inicio_entry.delete(0, tk.END)
                    self.anio_inicio_entry.insert(0, fecha.year)

            if 'fecha_fin' in exposicion and exposicion['fecha_fin']:
                fecha = exposicion['fecha_fin']
                if isinstance(fecha, datetime):
                    self.dia_fin_entry.delete(0, tk.END)
                    self.dia_fin_entry.insert(0, fecha.day)
                    self.mes_fin_entry.delete(0, tk.END)
                    self.mes_fin_entry.insert(0, fecha.month)
                    self.anio_fin_entry.delete(0, tk.END)
                    self.anio_fin_entry.insert(0, fecha.year)

            self.descripcion_text.delete(1.0, tk.END)
            self.descripcion_text.insert(1.0, exposicion.get('descripcion', ''))

            # Cargar obras seleccionadas
            self.obras_seleccionadas = [str(oid) for oid in exposicion.get('obras', [])]
            self.actualizar_listas_obras()

    def actualizar_listas_obras(self):
        """Actualiza las listas de obras disponibles y seleccionadas"""
        self.obras_listbox.delete(0, tk.END)
        self.obras_selec_listbox.delete(0, tk.END)

        obras = self.obras_collection.find().sort("titulo", 1)

        for obra in obras:
            obra_id = str(obra['_id'])
            titulo = obra.get('titulo', 'Sin título')

            artista_nombre = "Desconocido"
            if 'artista_id' in obra:
                artista = self.artistas_collection.find_one({'_id': ObjectId(obra['artista_id'])})
                if artista:
                    artista_nombre = artista['nombre']

            display_text = f"{titulo} - {artista_nombre}"
            self.obras_dict[display_text] = obra_id

            if obra_id in self.obras_seleccionadas:
                self.obras_selec_listbox.insert(tk.END, display_text)
            else:
                self.obras_listbox.insert(tk.END, display_text)

    def nueva_exposicion(self):
        """Prepara el formulario para una nueva exposición"""
        self.limpiar_formulario()
        self.selected_exposicion_id = None

    def guardar_exposicion(self):
        """Guarda una nueva exposición"""
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio")
            return

        try:
            dia_i = int(self.dia_inicio_entry.get()) if self.dia_inicio_entry.get() else 1
            mes_i = int(self.mes_inicio_entry.get()) if self.mes_inicio_entry.get() else 1
            anio_i = int(self.anio_inicio_entry.get()) if self.anio_inicio_entry.get() else 2024
            fecha_inicio = datetime(anio_i, mes_i, dia_i)

            dia_f = int(self.dia_fin_entry.get()) if self.dia_fin_entry.get() else 1
            mes_f = int(self.mes_fin_entry.get()) if self.mes_fin_entry.get() else 1
            anio_f = int(self.anio_fin_entry.get()) if self.anio_fin_entry.get() else 2024
            fecha_fin = datetime(anio_f, mes_f, dia_f)
        except ValueError:
            messagebox.showerror("Error", "Fechas inválidas")
            return

        exposicion_data = {
            'nombre': nombre,
            'tema': self.tema_entry.get().strip(),
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'descripcion': self.descripcion_text.get(1.0, tk.END).strip(),
            'obras': [ObjectId(oid) for oid in self.obras_seleccionadas]
        }

        self.exposiciones_collection.insert_one(exposicion_data)
        messagebox.showinfo("Éxito", "Exposición guardada correctamente")

        self.load_exposiciones()
        self.limpiar_formulario()

    def actualizar_exposicion(self):
        """Actualiza una exposición existente"""
        if not self.selected_exposicion_id:
            messagebox.showwarning("Advertencia", "Selecciona una exposición para actualizar")
            return

        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio")
            return

        try:
            dia_i = int(self.dia_inicio_entry.get()) if self.dia_inicio_entry.get() else 1
            mes_i = int(self.mes_inicio_entry.get()) if self.mes_inicio_entry.get() else 1
            anio_i = int(self.anio_inicio_entry.get()) if self.anio_inicio_entry.get() else 2024
            fecha_inicio = datetime(anio_i, mes_i, dia_i)

            dia_f = int(self.dia_fin_entry.get()) if self.dia_fin_entry.get() else 1
            mes_f = int(self.mes_fin_entry.get()) if self.mes_fin_entry.get() else 1
            anio_f = int(self.anio_fin_entry.get()) if self.anio_fin_entry.get() else 2024
            fecha_fin = datetime(anio_f, mes_f, dia_f)
        except ValueError:
            messagebox.showerror("Error", "Fechas inválidas")
            return

        exposicion_data = {
            'nombre': nombre,
            'tema': self.tema_entry.get().strip(),
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'descripcion': self.descripcion_text.get(1.0, tk.END).strip(),
            'obras': [ObjectId(oid) for oid in self.obras_seleccionadas]
        }

        self.exposiciones_collection.update_one(
            {'_id': ObjectId(self.selected_exposicion_id)},
            {'$set': exposicion_data}
        )

        messagebox.showinfo("Éxito", "Exposición actualizada correctamente")
        self.load_exposiciones()

    def eliminar_exposicion(self):
        """Elimina una exposición"""
        if not self.selected_exposicion_id:
            messagebox.showwarning("Advertencia", "Selecciona una exposición para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta exposición?"):
            self.exposiciones_collection.delete_one({'_id': ObjectId(self.selected_exposicion_id)})
            messagebox.showinfo("Éxito", "Exposición eliminada correctamente")

            self.load_exposiciones()
            self.limpiar_formulario()
            self.selected_exposicion_id = None

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.nombre_entry.delete(0, tk.END)
        self.tema_entry.delete(0, tk.END)
        self.dia_inicio_entry.delete(0, tk.END)
        self.mes_inicio_entry.delete(0, tk.END)
        self.anio_inicio_entry.delete(0, tk.END)
        self.dia_fin_entry.delete(0, tk.END)
        self.mes_fin_entry.delete(0, tk.END)
        self.anio_fin_entry.delete(0, tk.END)
        self.descripcion_text.delete(1.0, tk.END)

        self.obras_seleccionadas = []
        self.load_obras_disponibles()
        self.obras_selec_listbox.delete(0, tk.END)

        self.selected_exposicion_id = None
