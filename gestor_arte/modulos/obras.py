"""
Módulo 2: Catálogo de Obras
Ingreso de obras con metadatos específicos según la técnica
Actor: Curador
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from database import get_db
from bson.objectid import ObjectId
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import configure_styles, COLORS, FONTS

class ObrasWindow:
    def __init__(self):
        """Inicializa la ventana de gestión de obras"""
        self.window = tk.Toplevel()
        self.window.title("Catálogo de Obras")
        self.window.geometry("1200x750")
        self.window.configure(bg=COLORS['bg_primary'])

        # Configurar estilos
        configure_styles()

        self.db = get_db()
        self.obras_collection = self.db.get_collection('obras')
        self.artistas_collection = self.db.get_collection('artistas')

        self.selected_obra_id = None
        self.metadatos_widgets = {}

        self.setup_ui()
        self.load_obras()
        self.load_artistas()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Header
        header_frame = tk.Frame(self.window, bg='#9B59B6', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Título en el header
        title_label = tk.Label(
            header_frame,
            text="🎨 CATÁLOGO DE OBRAS",
            font=('Segoe UI', 20, 'bold'),
            bg='#9B59B6',
            fg=COLORS['text_light']
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=30)

        subtitle_label = tk.Label(
            header_frame,
            text="Gestión de obras con metadatos específicos por técnica",
            font=('Segoe UI', 10),
            bg='#9B59B6',
            fg=COLORS['text_light']
        )
        subtitle_label.pack(side=tk.LEFT, padx=(0, 30), pady=30)

        # Frame principal
        main_frame = tk.Frame(self.window, bg=COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel izquierdo - Lista de obras
        left_panel = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Título del panel izquierdo
        left_title_frame = tk.Frame(left_panel, bg=COLORS['bg_secondary'], height=50)
        left_title_frame.pack(fill=tk.X, pady=(0, 5))
        left_title_frame.pack_propagate(False)

        tk.Label(
            left_title_frame,
            text="Lista de Obras",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).pack(side=tk.LEFT, padx=15, pady=10)

        # Treeview con estilo
        tree_frame = tk.Frame(left_panel, bg=COLORS['bg_secondary'], relief='solid', borderwidth=1)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview
        columns = ("titulo", "artista", "tecnica", "año")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings", height=20)

        self.tree.heading("#0", text="ID")
        self.tree.heading("titulo", text="Título")
        self.tree.heading("artista", text="Artista")
        self.tree.heading("tecnica", text="Técnica")
        self.tree.heading("año", text="Año")

        self.tree.column("#0", width=50)
        self.tree.column("titulo", width=200)
        self.tree.column("artista", width=150)
        self.tree.column("tecnica", width=100)
        self.tree.column("año", width=80)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<<TreeviewSelect>>', self.on_select_obra)

        # Panel derecho - Formulario
        right_panel = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Título del panel derecho
        right_title_frame = tk.Frame(right_panel, bg=COLORS['bg_secondary'], height=50)
        right_title_frame.pack(fill=tk.X, pady=(0, 5))
        right_title_frame.pack_propagate(False)

        tk.Label(
            right_title_frame,
            text="Datos de la Obra",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).pack(side=tk.LEFT, padx=15, pady=10)

        # Formulario con fondo y scroll
        form_frame = tk.Frame(right_panel, bg=COLORS['bg_secondary'], relief='solid', borderwidth=1)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Canvas para scroll
        canvas = tk.Canvas(form_frame, bg=COLORS['bg_secondary'], highlightthickness=0)
        scrollbar_form = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)

        form_content = tk.Frame(canvas, bg=COLORS['bg_secondary'])

        form_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=form_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_form.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=25, pady=20)
        scrollbar_form.pack(side=tk.RIGHT, fill=tk.Y)

        row = 0

        # Título
        tk.Label(
            form_content,
            text="Título:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(10, 5))

        self.titulo_entry = tk.Entry(
            form_content,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.titulo_entry.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15), ipady=8)
        row += 2

        # Artista
        tk.Label(
            form_content,
            text="Artista:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        self.artista_combo = ttk.Combobox(form_content, state="readonly", font=('Segoe UI', 10))
        self.artista_combo.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15), ipady=8)
        row += 2

        # Técnica
        tk.Label(
            form_content,
            text="Técnica:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        self.tecnica_combo = ttk.Combobox(
            form_content,
            values=["Pintura", "Escultura", "Fotografía", "Grabado", "Arte Digital", "Instalación"],
            state="readonly",
            font=('Segoe UI', 10)
        )
        self.tecnica_combo.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15), ipady=8)
        self.tecnica_combo.bind('<<ComboboxSelected>>', self.on_tecnica_change)
        row += 2

        # Año
        tk.Label(
            form_content,
            text="Año:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        self.anio_entry = tk.Entry(
            form_content,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.anio_entry.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15), ipady=8)
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
        separator.grid(row=row, column=0, sticky=tk.EW, pady=15)
        row += 1

        # Título metadatos
        tk.Label(
            form_content,
            text="Metadatos Específicos:",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(0, 10))
        row += 1

        # Frame para metadatos dinámicos
        self.metadatos_frame = tk.Frame(form_content, bg=COLORS['bg_secondary'])
        self.metadatos_frame.grid(row=row, column=0, sticky=tk.EW, pady=5)
        row += 1

        # Configurar expansión
        form_content.columnconfigure(0, weight=1)

        # Botones de acción
        buttons_frame = tk.Frame(form_content, bg=COLORS['bg_secondary'])
        buttons_frame.grid(row=row, column=0, sticky=tk.EW, pady=(20, 10))

        # Crear botones con estilos
        btn_config = [
            ("Nuevo", self.nueva_obra, COLORS['accent']),
            ("Guardar", self.guardar_obra, COLORS['success']),
            ("Actualizar", self.actualizar_obra, COLORS['warning']),
            ("Eliminar", self.eliminar_obra, COLORS['danger']),
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

    def on_tecnica_change(self, event):
        """Actualiza los campos de metadatos según la técnica seleccionada"""
        self.update_metadatos_fields()

    def update_metadatos_fields(self):
        """Actualiza los campos de metadatos específicos según la técnica"""
        # Limpiar frame de metadatos
        for widget in self.metadatos_frame.winfo_children():
            widget.destroy()
        self.metadatos_widgets.clear()

        tecnica = self.tecnica_combo.get()
        row = 0

        if tecnica == "Pintura":
            # Pigmento
            tk.Label(
                self.metadatos_frame,
                text="Pigmento:",
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_primary']
            ).grid(row=row, column=0, sticky=tk.W, pady=5)

            self.metadatos_widgets['pigmento'] = tk.Entry(
                self.metadatos_frame,
                font=('Segoe UI', 10),
                relief='solid',
                borderwidth=1,
                highlightthickness=2,
                highlightbackground=COLORS['border'],
                highlightcolor=COLORS['accent']
            )
            self.metadatos_widgets['pigmento'].grid(row=row, column=1, pady=5, sticky=tk.EW, ipady=6)
            row += 1

            # Dimensiones
            tk.Label(
                self.metadatos_frame,
                text="Dimensiones:",
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_primary']
            ).grid(row=row, column=0, sticky=tk.W, pady=5)

            self.metadatos_widgets['dimensiones'] = tk.Entry(
                self.metadatos_frame,
                font=('Segoe UI', 10),
                relief='solid',
                borderwidth=1,
                highlightthickness=2,
                highlightbackground=COLORS['border'],
                highlightcolor=COLORS['accent']
            )
            self.metadatos_widgets['dimensiones'].grid(row=row, column=1, pady=5, sticky=tk.EW, ipady=6)
            row += 1

            # Soporte
            tk.Label(
                self.metadatos_frame,
                text="Soporte:",
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_primary']
            ).grid(row=row, column=0, sticky=tk.W, pady=5)

            self.metadatos_widgets['soporte'] = tk.Entry(
                self.metadatos_frame,
                font=('Segoe UI', 10),
                relief='solid',
                borderwidth=1,
                highlightthickness=2,
                highlightbackground=COLORS['border'],
                highlightcolor=COLORS['accent']
            )
            self.metadatos_widgets['soporte'].grid(row=row, column=1, pady=5, sticky=tk.EW, ipady=6)

        elif tecnica == "Escultura":
            # Material
            tk.Label(
                self.metadatos_frame,
                text="Material:",
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_primary']
            ).grid(row=row, column=0, sticky=tk.W, pady=5)

            self.metadatos_widgets['material'] = tk.Entry(
                self.metadatos_frame,
                font=('Segoe UI', 10),
                relief='solid',
                borderwidth=1,
                highlightthickness=2,
                highlightbackground=COLORS['border'],
                highlightcolor=COLORS['accent']
            )
            self.metadatos_widgets['material'].grid(row=row, column=1, pady=5, sticky=tk.EW, ipady=6)
            row += 1

            # Dimensiones
            tk.Label(
                self.metadatos_frame,
                text="Dimensiones:",
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_primary']
            ).grid(row=row, column=0, sticky=tk.W, pady=5)

            self.metadatos_widgets['dimensiones'] = tk.Entry(
                self.metadatos_frame,
                font=('Segoe UI', 10),
                relief='solid',
                borderwidth=1,
                highlightthickness=2,
                highlightbackground=COLORS['border'],
                highlightcolor=COLORS['accent']
            )
            self.metadatos_widgets['dimensiones'].grid(row=row, column=1, pady=5, sticky=tk.EW, ipady=6)
            row += 1

            # Peso
            tk.Label(
                self.metadatos_frame,
                text="Peso:",
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_primary']
            ).grid(row=row, column=0, sticky=tk.W, pady=5)

            self.metadatos_widgets['peso'] = tk.Entry(
                self.metadatos_frame,
                font=('Segoe UI', 10),
                relief='solid',
                borderwidth=1,
                highlightthickness=2,
                highlightbackground=COLORS['border'],
                highlightcolor=COLORS['accent']
            )
            self.metadatos_widgets['peso'].grid(row=row, column=1, pady=5, sticky=tk.EW, ipady=6)

        elif tecnica == "Fotografía":
            # Técnica fotográfica
            tk.Label(
                self.metadatos_frame,
                text="Técnica Fotográfica:",
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_primary']
            ).grid(row=row, column=0, sticky=tk.W, pady=5)

            self.metadatos_widgets['tecnica_fotografica'] = tk.Entry(
                self.metadatos_frame,
                font=('Segoe UI', 10),
                relief='solid',
                borderwidth=1,
                highlightthickness=2,
                highlightbackground=COLORS['border'],
                highlightcolor=COLORS['accent']
            )
            self.metadatos_widgets['tecnica_fotografica'].grid(row=row, column=1, pady=5, sticky=tk.EW, ipady=6)
            row += 1

            # Formato
            tk.Label(
                self.metadatos_frame,
                text="Formato:",
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_primary']
            ).grid(row=row, column=0, sticky=tk.W, pady=5)

            self.metadatos_widgets['formato'] = tk.Entry(
                self.metadatos_frame,
                font=('Segoe UI', 10),
                relief='solid',
                borderwidth=1,
                highlightthickness=2,
                highlightbackground=COLORS['border'],
                highlightcolor=COLORS['accent']
            )
            self.metadatos_widgets['formato'].grid(row=row, column=1, pady=5, sticky=tk.EW, ipady=6)
            row += 1

            # Edición
            tk.Label(
                self.metadatos_frame,
                text="Edición:",
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_primary']
            ).grid(row=row, column=0, sticky=tk.W, pady=5)

            self.metadatos_widgets['edicion'] = tk.Entry(
                self.metadatos_frame,
                font=('Segoe UI', 10),
                relief='solid',
                borderwidth=1,
                highlightthickness=2,
                highlightbackground=COLORS['border'],
                highlightcolor=COLORS['accent']
            )
            self.metadatos_widgets['edicion'].grid(row=row, column=1, pady=5, sticky=tk.EW, ipady=6)

        else:
            # Campos genéricos para otras técnicas
            tk.Label(
                self.metadatos_frame,
                text="Materiales:",
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_primary']
            ).grid(row=row, column=0, sticky=tk.W, pady=5)

            self.metadatos_widgets['materiales'] = tk.Entry(
                self.metadatos_frame,
                font=('Segoe UI', 10),
                relief='solid',
                borderwidth=1,
                highlightthickness=2,
                highlightbackground=COLORS['border'],
                highlightcolor=COLORS['accent']
            )
            self.metadatos_widgets['materiales'].grid(row=row, column=1, pady=5, sticky=tk.EW, ipady=6)
            row += 1

            tk.Label(
                self.metadatos_frame,
                text="Dimensiones:",
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_primary']
            ).grid(row=row, column=0, sticky=tk.W, pady=5)

            self.metadatos_widgets['dimensiones'] = tk.Entry(
                self.metadatos_frame,
                font=('Segoe UI', 10),
                relief='solid',
                borderwidth=1,
                highlightthickness=2,
                highlightbackground=COLORS['border'],
                highlightcolor=COLORS['accent']
            )
            self.metadatos_widgets['dimensiones'].grid(row=row, column=1, pady=5, sticky=tk.EW, ipady=6)

        self.metadatos_frame.columnconfigure(1, weight=1)

    def load_artistas(self):
        """Carga los artistas en el ComboBox"""
        artistas = self.artistas_collection.find().sort("nombre", 1)
        self.artistas_dict = {}

        for artista in artistas:
            self.artistas_dict[artista['nombre']] = str(artista['_id'])

        self.artista_combo['values'] = list(self.artistas_dict.keys())

    def load_obras(self):
        """Carga todas las obras en el TreeView"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        obras = self.obras_collection.find().sort("titulo", 1)

        for idx, obra in enumerate(obras, 1):
            artista_nombre = "Desconocido"
            if 'artista_id' in obra:
                artista = self.artistas_collection.find_one({'_id': ObjectId(obra['artista_id'])})
                if artista:
                    artista_nombre = artista['nombre']

            self.tree.insert("", tk.END, iid=str(obra['_id']), text=str(idx),
                           values=(obra.get('titulo', ''),
                                 artista_nombre,
                                 obra.get('tecnica', ''),
                                 obra.get('anio', '')))

    def on_select_obra(self, event):
        """Maneja la selección de una obra en el TreeView"""
        selection = self.tree.selection()
        if selection:
            obra_id = selection[0]
            self.selected_obra_id = obra_id
            self.load_obra_data(obra_id)

    def load_obra_data(self, obra_id):
        """Carga los datos de una obra en el formulario"""
        obra = self.obras_collection.find_one({'_id': ObjectId(obra_id)})

        if obra:
            self.titulo_entry.delete(0, tk.END)
            self.titulo_entry.insert(0, obra.get('titulo', ''))

            # Seleccionar artista
            if 'artista_id' in obra:
                artista = self.artistas_collection.find_one({'_id': ObjectId(obra['artista_id'])})
                if artista:
                    self.artista_combo.set(artista['nombre'])

            # Seleccionar técnica
            if 'tecnica' in obra:
                self.tecnica_combo.set(obra['tecnica'])
                self.update_metadatos_fields()

            self.anio_entry.delete(0, tk.END)
            self.anio_entry.insert(0, str(obra.get('anio', '')))

            self.descripcion_text.delete(1.0, tk.END)
            self.descripcion_text.insert(1.0, obra.get('descripcion', ''))

            # Cargar metadatos
            if 'metadatos' in obra:
                for key, widget in self.metadatos_widgets.items():
                    if key in obra['metadatos']:
                        widget.delete(0, tk.END)
                        widget.insert(0, obra['metadatos'][key])

    def nueva_obra(self):
        """Prepara el formulario para una nueva obra"""
        self.limpiar_formulario()
        self.selected_obra_id = None

    def guardar_obra(self):
        """Guarda una nueva obra"""
        titulo = self.titulo_entry.get().strip()
        if not titulo:
            messagebox.showwarning("Advertencia", "El título es obligatorio")
            return

        artista_nombre = self.artista_combo.get()
        if not artista_nombre:
            messagebox.showwarning("Advertencia", "Debes seleccionar un artista")
            return

        tecnica = self.tecnica_combo.get()
        if not tecnica:
            messagebox.showwarning("Advertencia", "Debes seleccionar una técnica")
            return

        try:
            anio = int(self.anio_entry.get()) if self.anio_entry.get() else None
        except ValueError:
            messagebox.showerror("Error", "El año debe ser un número")
            return

        # Recopilar metadatos
        metadatos = {}
        for key, widget in self.metadatos_widgets.items():
            valor = widget.get().strip()
            if valor:
                metadatos[key] = valor

        obra_data = {
            'titulo': titulo,
            'artista_id': self.artistas_dict[artista_nombre],
            'tecnica': tecnica,
            'anio': anio,
            'descripcion': self.descripcion_text.get(1.0, tk.END).strip(),
            'metadatos': metadatos
        }

        self.obras_collection.insert_one(obra_data)
        messagebox.showinfo("Éxito", "Obra guardada correctamente")

        self.load_obras()
        self.limpiar_formulario()

    def actualizar_obra(self):
        """Actualiza una obra existente"""
        if not self.selected_obra_id:
            messagebox.showwarning("Advertencia", "Selecciona una obra para actualizar")
            return

        titulo = self.titulo_entry.get().strip()
        if not titulo:
            messagebox.showwarning("Advertencia", "El título es obligatorio")
            return

        artista_nombre = self.artista_combo.get()
        if not artista_nombre:
            messagebox.showwarning("Advertencia", "Debes seleccionar un artista")
            return

        tecnica = self.tecnica_combo.get()
        if not tecnica:
            messagebox.showwarning("Advertencia", "Debes seleccionar una técnica")
            return

        try:
            anio = int(self.anio_entry.get()) if self.anio_entry.get() else None
        except ValueError:
            messagebox.showerror("Error", "El año debe ser un número")
            return

        metadatos = {}
        for key, widget in self.metadatos_widgets.items():
            valor = widget.get().strip()
            if valor:
                metadatos[key] = valor

        obra_data = {
            'titulo': titulo,
            'artista_id': self.artistas_dict[artista_nombre],
            'tecnica': tecnica,
            'anio': anio,
            'descripcion': self.descripcion_text.get(1.0, tk.END).strip(),
            'metadatos': metadatos
        }

        self.obras_collection.update_one(
            {'_id': ObjectId(self.selected_obra_id)},
            {'$set': obra_data}
        )

        messagebox.showinfo("Éxito", "Obra actualizada correctamente")
        self.load_obras()

    def eliminar_obra(self):
        """Elimina una obra"""
        if not self.selected_obra_id:
            messagebox.showwarning("Advertencia", "Selecciona una obra para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta obra?"):
            self.obras_collection.delete_one({'_id': ObjectId(self.selected_obra_id)})
            messagebox.showinfo("Éxito", "Obra eliminada correctamente")

            self.load_obras()
            self.limpiar_formulario()
            self.selected_obra_id = None

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.titulo_entry.delete(0, tk.END)
        self.artista_combo.set('')
        self.tecnica_combo.set('')
        self.anio_entry.delete(0, tk.END)
        self.descripcion_text.delete(1.0, tk.END)

        for widget in self.metadatos_frame.winfo_children():
            widget.destroy()
        self.metadatos_widgets.clear()

        self.selected_obra_id = None
