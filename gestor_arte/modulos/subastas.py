"""
Módulo 4: Valoraciones y Subastas
Registro de la valoración de una obra y el historial de ofertas de subasta
Actor: Administrador
"""
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_db
from bson.objectid import ObjectId
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import configure_styles, COLORS, FONTS

class SubastasWindow:
    def __init__(self):
        """Inicializa la ventana de gestión de subastas"""
        self.window = tk.Toplevel()
        self.window.title("Valoraciones y Subastas")
        self.window.geometry("1300x750")
        self.window.configure(bg=COLORS['bg_primary'])

        # Configurar estilos
        configure_styles()

        self.db = get_db()
        self.valoraciones_collection = self.db.get_collection('valoraciones')
        self.obras_collection = self.db.get_collection('obras')
        self.artistas_collection = self.db.get_collection('artistas')

        self.selected_valoracion_id = None
        self.current_obra_id = None

        self.setup_ui()
        self.load_valoraciones()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Header
        header_frame = tk.Frame(self.window, bg='#27AE60', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # MARCO: Ajuste de diseño y color del Header para la identidad visual del Módulo 4.
        
        # Título en el header
        title_label = tk.Label(
            header_frame,
            text="💰 VALORACIONES Y SUBASTAS",
            font=('Segoe UI', 20, 'bold'),
            bg='#27AE60',
            fg=COLORS['text_light']
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=30)

        subtitle_label = tk.Label(
            header_frame,
            text="Gestión de valoraciones y registro de ofertas de subasta",
            font=('Segoe UI', 10),
            bg='#27AE60',
            fg=COLORS['text_light']
        )
        subtitle_label.pack(side=tk.LEFT, padx=(0, 30), pady=30)

        # Frame principal
        main_frame = tk.Frame(self.window, bg=COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel izquierdo - Lista de valoraciones
        left_panel = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Título del panel izquierdo
        left_title_frame = tk.Frame(left_panel, bg=COLORS['bg_secondary'], height=50)
        left_title_frame.pack(fill=tk.X, pady=(0, 5))
        left_title_frame.pack_propagate(False)

        tk.Label(
            left_title_frame,
            text="Obras con Valoración",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).pack(side=tk.LEFT, padx=15, pady=10)

        # Treeview con estilo
        tree_frame = tk.Frame(left_panel, bg=COLORS['bg_secondary'], relief='solid', borderwidth=1)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview
        columns = ("obra", "artista", "valoracion", "ofertas")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings", height=20)

        self.tree.heading("#0", text="ID")
        self.tree.heading("obra", text="Obra")
        self.tree.heading("artista", text="Artista")
        self.tree.heading("valoracion", text="Valoración")
        self.tree.heading("ofertas", text="Ofertas")

        self.tree.column("#0", width=40)
        self.tree.column("obra", width=200)
        self.tree.column("artista", width=150)
        self.tree.column("valoracion", width=100)
        self.tree.column("ofertas", width=80)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<<TreeviewSelect>>', self.on_select_valoracion)

        # Panel derecho - Formularios
        right_panel = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Sección 1: Valoración
        val_title_frame = tk.Frame(right_panel, bg=COLORS['bg_secondary'], height=50)
        val_title_frame.pack(fill=tk.X, pady=(0, 5))
        val_title_frame.pack_propagate(False)

        tk.Label(
            val_title_frame,
            text="Valoración de la Obra",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).pack(side=tk.LEFT, padx=15, pady=10)

        # Formulario valoración
        valoracion_frame = tk.Frame(right_panel, bg=COLORS['bg_secondary'], relief='solid', borderwidth=1)
        valoracion_frame.pack(fill=tk.X, padx=0, pady=(0, 10))

        val_content = tk.Frame(valoracion_frame, bg=COLORS['bg_secondary'])
        val_content.pack(fill=tk.X, padx=20, pady=15)

        row = 0

        # Obra
        tk.Label(val_content, text="Obra:", font=('Segoe UI', 10, 'bold'), bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))
        self.obra_combo = ttk.Combobox(val_content, state="readonly", font=('Segoe UI', 10))
        self.obra_combo.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 10), ipady=6)
        self.obra_combo.bind('<<ComboboxSelected>>', self.on_obra_selected)
        row += 2

        # Valoración y moneda en una fila
        tk.Label(val_content, text="Valoración Actual:", font=('Segoe UI', 10, 'bold'), bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        val_row_frame = tk.Frame(val_content, bg=COLORS['bg_secondary'])
        val_row_frame.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 10))

        tk.Label(val_row_frame, text="$", bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], font=('Segoe UI', 11)).pack(side=tk.LEFT)
        self.valoracion_entry = tk.Entry(val_row_frame, font=('Segoe UI', 11), relief='solid', borderwidth=1, highlightthickness=2, highlightbackground=COLORS['border'], highlightcolor=COLORS['accent'])
        self.valoracion_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 10), ipady=6)

        tk.Label(val_row_frame, text="Moneda:", bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT)
        self.moneda_combo = ttk.Combobox(val_row_frame, values=["USD", "EUR", "MXN", "ARS", "COP"], state="readonly", font=('Segoe UI', 10), width=8)
        self.moneda_combo.current(0)
        self.moneda_combo.pack(side=tk.LEFT, padx=(2, 0), ipady=6)
        row += 2

        # Fecha y perito en una fila
        fecha_perito_frame = tk.Frame(val_content, bg=COLORS['bg_secondary'])
        fecha_perito_frame.grid(row=row, column=0, sticky=tk.EW, pady=(0, 10))

        # Fecha
        fecha_col = tk.Frame(fecha_perito_frame, bg=COLORS['bg_secondary'])
        fecha_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(fecha_col, text="F. Valoración:", font=('Segoe UI', 9, 'bold'), bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(anchor=tk.W)
        fecha_entries = tk.Frame(fecha_col, bg=COLORS['bg_secondary'])
        fecha_entries.pack(fill=tk.X, pady=(5, 0))

        tk.Label(fecha_entries, text="D:", bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT)
        self.dia_val_entry = tk.Entry(fecha_entries, width=4, font=('Segoe UI', 10))
        self.dia_val_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(fecha_entries, text="M:", bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT, padx=(5, 0))
        self.mes_val_entry = tk.Entry(fecha_entries, width=4, font=('Segoe UI', 10))
        self.mes_val_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(fecha_entries, text="A:", bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT, padx=(5, 0))
        self.anio_val_entry = tk.Entry(fecha_entries, width=6, font=('Segoe UI', 10))
        self.anio_val_entry.pack(side=tk.LEFT, padx=2)

        # Perito
        perito_col = tk.Frame(fecha_perito_frame, bg=COLORS['bg_secondary'])
        perito_col.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(perito_col, text="Perito/Tasador:", font=('Segoe UI', 9, 'bold'), bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(anchor=tk.W)
        self.perito_entry = tk.Entry(perito_col, font=('Segoe UI', 10), relief='solid', borderwidth=1, highlightthickness=2, highlightbackground=COLORS['border'], highlightcolor=COLORS['accent'])
        self.perito_entry.pack(fill=tk.X, pady=(5, 0), ipady=6)
        row += 1

        val_content.columnconfigure(0, weight=1)

        # Botones valoración
        val_buttons = tk.Frame(val_content, bg=COLORS['bg_secondary'])
        val_buttons.grid(row=row, column=0, sticky=tk.EW, pady=(10, 5))

        btn_val_config = [
            ("Nueva Valoración", self.nueva_valoracion, COLORS['accent']),
            ("Guardar", self.guardar_valoracion, COLORS['success']),
            ("Actualizar", self.actualizar_valoracion, COLORS['warning'])
        ]

        for idx, (text, command, color) in enumerate(btn_val_config):
            btn = tk.Button(val_buttons, text=text, font=('Segoe UI', 9, 'bold'), bg=color, fg=COLORS['text_light'], relief='flat', cursor='hand2', command=command)
            btn.grid(row=0, column=idx, padx=3, sticky=tk.EW, ipady=6)
            val_buttons.columnconfigure(idx, weight=1)

            def make_hover(button, base_color):
                def on_enter(e):
                    button['bg'] = self.lighten_color(base_color)
                def on_leave(e):
                    button['bg'] = base_color
                button.bind("<Enter>", on_enter)
                button.bind("<Leave>", on_leave)

            make_hover(btn, color)

        # Sección 2: Nueva Oferta
        oferta_title_frame = tk.Frame(right_panel, bg=COLORS['bg_secondary'], height=40)
        oferta_title_frame.pack(fill=tk.X, pady=(10, 5))
        oferta_title_frame.pack_propagate(False)

        tk.Label(
            oferta_title_frame,
            text="Nueva Oferta de Subasta",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).pack(side=tk.LEFT, padx=15, pady=8)

        # Formulario oferta
        oferta_frame = tk.Frame(right_panel, bg=COLORS['bg_secondary'], relief='solid', borderwidth=1)
        oferta_frame.pack(fill=tk.X, padx=0, pady=(0, 10))

        oferta_content = tk.Frame(oferta_frame, bg=COLORS['bg_secondary'])
        oferta_content.pack(fill=tk.X, padx=20, pady=15)

        # Ofertante y monto en columnas
        oferta_row = tk.Frame(oferta_content, bg=COLORS['bg_secondary'])
        oferta_row.pack(fill=tk.X)

        # Ofertante
        ofertante_col = tk.Frame(oferta_row, bg=COLORS['bg_secondary'])
        ofertante_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(ofertante_col, text="Ofertante:", font=('Segoe UI', 10, 'bold'), bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(anchor=tk.W, pady=(0, 5))
        self.ofertante_entry = tk.Entry(ofertante_col, font=('Segoe UI', 11), relief='solid', borderwidth=1, highlightthickness=2, highlightbackground=COLORS['border'], highlightcolor=COLORS['accent'])
        self.ofertante_entry.pack(fill=tk.X, ipady=6)

        # Monto
        monto_col = tk.Frame(oferta_row, bg=COLORS['bg_secondary'])
        monto_col.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(monto_col, text="Monto Oferta:", font=('Segoe UI', 10, 'bold'), bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(anchor=tk.W, pady=(0, 5))
        monto_entry_frame = tk.Frame(monto_col, bg=COLORS['bg_secondary'])
        monto_entry_frame.pack(fill=tk.X)

        tk.Label(monto_entry_frame, text="$", bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], font=('Segoe UI', 11)).pack(side=tk.LEFT)
        self.monto_oferta_entry = tk.Entry(monto_entry_frame, font=('Segoe UI', 11), relief='solid', borderwidth=1, highlightthickness=2, highlightbackground=COLORS['border'], highlightcolor=COLORS['accent'])
        self.monto_oferta_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, ipady=6)

        # Botón agregar oferta
        tk.Button(oferta_content, text="Agregar Oferta", font=('Segoe UI', 10, 'bold'), bg=COLORS['success'], fg=COLORS['text_light'], relief='flat', cursor='hand2', command=self.agregar_oferta).pack(pady=(15, 5), fill=tk.X, ipady=8)

        # Sección 3: Historial de Ofertas
        historial_title_frame = tk.Frame(right_panel, bg=COLORS['bg_secondary'], height=40)
        historial_title_frame.pack(fill=tk.X, pady=(10, 5))
        historial_title_frame.pack_propagate(False)

        tk.Label(
            historial_title_frame,
            text="Historial de Ofertas",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).pack(side=tk.LEFT, padx=15, pady=8)

        # Treeview historial
        historial_frame = tk.Frame(right_panel, bg=COLORS['bg_secondary'], relief='solid', borderwidth=1)
        historial_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 10))

        ofertas_columns = ("fecha", "ofertante", "monto")
        self.ofertas_tree = ttk.Treeview(historial_frame, columns=ofertas_columns, show="headings", height=8)

        self.ofertas_tree.heading("fecha", text="Fecha")
        self.ofertas_tree.heading("ofertante", text="Ofertante")
        self.ofertas_tree.heading("monto", text="Monto")

        self.ofertas_tree.column("fecha", width=150)
        self.ofertas_tree.column("ofertante", width=200)
        self.ofertas_tree.column("monto", width=120)

        scrollbar_ofertas = ttk.Scrollbar(historial_frame, orient=tk.VERTICAL, command=self.ofertas_tree.yview)
        self.ofertas_tree.configure(yscrollcommand=scrollbar_ofertas.set)

        self.ofertas_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        scrollbar_ofertas.pack(side=tk.RIGHT, fill=tk.Y)

        # Botones finales
        final_buttons = tk.Frame(right_panel, bg=COLORS['bg_primary'])
        final_buttons.pack(fill=tk.X, pady=(5, 0))

        btn_final_config = [
            ("Eliminar Oferta", self.eliminar_oferta, COLORS['danger']),
            ("Eliminar Valoración", self.eliminar_valoracion, COLORS['danger']),
            ("Limpiar", self.limpiar_formulario, COLORS['text_secondary'])
        ]

        for idx, (text, command, color) in enumerate(btn_final_config):
            btn = tk.Button(final_buttons, text=text, font=('Segoe UI', 10, 'bold'), bg=color, fg=COLORS['text_light'], relief='flat', cursor='hand2', command=command)
            btn.grid(row=0, column=idx, padx=3, sticky=tk.EW, ipady=8)
            final_buttons.columnconfigure(idx, weight=1)

            make_hover(btn, color)

        # Cargar obras
        self.load_obras_combo()

    def lighten_color(self, color):
        """Aclara un color hexadecimal"""
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'

    def load_obras_combo(self):
        """Carga las obras en el ComboBox"""
        obras = self.obras_collection.find().sort("titulo", 1)
        self.obras_dict = {}

        for obra in obras:
            titulo = obra.get('titulo', 'Sin título')
            artista_nombre = "Desconocido"

            if 'artista_id' in obra:
                artista = self.artistas_collection.find_one({'_id': ObjectId(obra['artista_id'])})
                if artista:
                    artista_nombre = artista['nombre']

            display_text = f"{titulo} - {artista_nombre}"
            self.obras_dict[display_text] = str(obra['_id'])

        self.obra_combo['values'] = list(self.obras_dict.keys())

    def on_obra_selected(self, event):
        """Maneja la selección de una obra"""
        obra_text = self.obra_combo.get()
        if obra_text:
            self.current_obra_id = self.obras_dict[obra_text]

            # Verificar si ya existe una valoración
            valoracion = self.valoraciones_collection.find_one({'obra_id': self.current_obra_id})
            if valoracion:
                self.selected_valoracion_id = str(valoracion['_id'])
                self.load_valoracion_data(self.selected_valoracion_id)

    def load_valoraciones(self):
        """Carga todas las valoraciones en el TreeView"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        valoraciones = self.valoraciones_collection.find()

        for idx, val in enumerate(valoraciones, 1):
            obra_titulo = "Desconocida"
            artista_nombre = "Desconocido"

            if 'obra_id' in val:
                obra = self.obras_collection.find_one({'_id': ObjectId(val['obra_id'])})
                if obra:
                    obra_titulo = obra.get('titulo', 'Sin título')

                    if 'artista_id' in obra:
                        artista = self.artistas_collection.find_one({'_id': ObjectId(obra['artista_id'])})
                        if artista:
                            artista_nombre = artista['nombre']

            valoracion_str = f"${val.get('valoracion_actual', 0)} {val.get('moneda', 'USD')}"
            num_ofertas = len(val.get('historial_ofertas', []))

            self.tree.insert("", tk.END, iid=str(val['_id']), text=str(idx),
                           values=(obra_titulo, artista_nombre, valoracion_str, num_ofertas))

    def on_select_valoracion(self, event):
        """Maneja la selección de una valoración en el TreeView"""
        selection = self.tree.selection()
        if selection:
            valoracion_id = selection[0]
            self.selected_valoracion_id = valoracion_id
            self.load_valoracion_data(valoracion_id)

    def load_valoracion_data(self, valoracion_id):
        """Carga los datos de una valoración en el formulario"""
        valoracion = self.valoraciones_collection.find_one({'_id': ObjectId(valoracion_id)})

        if valoracion:
            # Cargar obra
            if 'obra_id' in valoracion:
                self.current_obra_id = valoracion['obra_id']
                obra = self.obras_collection.find_one({'_id': ObjectId(valoracion['obra_id'])})

                if obra:
                    titulo = obra.get('titulo', 'Sin título')
                    artista_nombre = "Desconocido"

                    if 'artista_id' in obra:
                        artista = self.artistas_collection.find_one({'_id': ObjectId(obra['artista_id'])})
                        if artista:
                            artista_nombre = artista['nombre']

                    display_text = f"{titulo} - {artista_nombre}"
                    self.obra_combo.set(display_text)

            # Valoración
            self.valoracion_entry.delete(0, tk.END)
            self.valoracion_entry.insert(0, str(valoracion.get('valoracion_actual', '')))

            # Moneda
            if 'moneda' in valoracion:
                self.moneda_combo.set(valoracion['moneda'])

            # Fecha
            if 'fecha_valoracion' in valoracion and valoracion['fecha_valoracion']:
                fecha = valoracion['fecha_valoracion']
                if isinstance(fecha, datetime):
                    self.dia_val_entry.delete(0, tk.END)
                    self.dia_val_entry.insert(0, fecha.day)
                    self.mes_val_entry.delete(0, tk.END)
                    self.mes_val_entry.insert(0, fecha.month)
                    self.anio_val_entry.delete(0, tk.END)
                    self.anio_val_entry.insert(0, fecha.year)

            # Perito
            self.perito_entry.delete(0, tk.END)
            self.perito_entry.insert(0, valoracion.get('perito', ''))

            # Cargar historial de ofertas
            self.load_ofertas(valoracion.get('historial_ofertas', []))

    def load_ofertas(self, ofertas):
        """Carga el historial de ofertas en el TreeView"""
        for item in self.ofertas_tree.get_children():
            self.ofertas_tree.delete(item)

        for oferta in sorted(ofertas, key=lambda x: x.get('fecha', datetime.now()), reverse=True):
            fecha_str = oferta['fecha'].strftime("%d/%m/%Y %H:%M") if isinstance(oferta.get('fecha'), datetime) else "N/A"
            monto_str = f"${oferta.get('monto', 0)}"

            self.ofertas_tree.insert("", tk.END,
                                   values=(fecha_str, oferta.get('ofertante', ''), monto_str))

    def nueva_valoracion(self):
        """Prepara el formulario para una nueva valoración"""
        self.limpiar_formulario()
        self.selected_valoracion_id = None

    def guardar_valoracion(self):
        """Guarda una nueva valoración"""
        # MARCO: Verificación de la colección 'Valoraciones' antes de la inserción, cumpliendo con el estándar CRUD.
        if not self.current_obra_id:
            messagebox.showwarning("Advertencia", "Debes seleccionar una obra")
            return

        # Verificar si ya existe una valoración para esta obra
        existing = self.valoraciones_collection.find_one({'obra_id': self.current_obra_id})
        if existing:
            messagebox.showwarning("Advertencia", "Esta obra ya tiene una valoración. Usa 'Actualizar' para modificarla.")
            return

        try:
            valoracion = float(self.valoracion_entry.get())
        except ValueError:
            messagebox.showerror("Error", "La valoración debe ser un número")
            return

        try:
            dia = int(self.dia_val_entry.get()) if self.dia_val_entry.get() else datetime.now().day
            mes = int(self.mes_val_entry.get()) if self.mes_val_entry.get() else datetime.now().month
            anio = int(self.anio_val_entry.get()) if self.anio_val_entry.get() else datetime.now().year
            fecha_valoracion = datetime(anio, mes, dia)
        except ValueError:
            messagebox.showerror("Error", "Fecha inválida")
            return

        valoracion_data = {
            'obra_id': self.current_obra_id,
            'valoracion_actual': valoracion,
            'moneda': self.moneda_combo.get(),
            'fecha_valoracion': fecha_valoracion,
            'perito': self.perito_entry.get().strip(),
            'historial_ofertas': []
        }

        self.valoraciones_collection.insert_one(valoracion_data)
        messagebox.showinfo("Éxito", "Valoración guardada correctamente")

        self.load_valoraciones()

    def actualizar_valoracion(self):
        """Actualiza una valoración existente"""
        if not self.selected_valoracion_id:
            messagebox.showwarning("Advertencia", "Selecciona una valoración para actualizar")
            return

        try:
            monto = float(self.monto_oferta_entry.get())
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número")
            return
        
        # MARCO: Validación de monto positivo agregada para evitar errores lógicos.
        if monto <= 0:
            messagebox.showwarning("Advertencia", "El monto de la oferta debe ser mayor a cero.")
            return

        try:
            dia = int(self.dia_val_entry.get()) if self.dia_val_entry.get() else datetime.now().day
            mes = int(self.mes_val_entry.get()) if self.mes_val_entry.get() else datetime.now().month
            anio = int(self.anio_val_entry.get()) if self.anio_val_entry.get() else datetime.now().year
            fecha_valoracion = datetime(anio, mes, dia)
        except ValueError:
            messagebox.showerror("Error", "Fecha inválida")
            return

        self.valoraciones_collection.update_one(
            {'_id': ObjectId(self.selected_valoracion_id)},
            {'$set': {
                'valoracion_actual': valoracion,
                'moneda': self.moneda_combo.get(),
                'fecha_valoracion': fecha_valoracion,
                'perito': self.perito_entry.get().strip()
            }}
        )

        messagebox.showinfo("Éxito", "Valoración actualizada correctamente")
        self.load_valoraciones()

    def agregar_oferta(self):
        """Agrega una nueva oferta al historial"""
        if not self.selected_valoracion_id:
            messagebox.showwarning("Advertencia", "Primero debes seleccionar o crear una valoración")
            return

        ofertante = self.ofertante_entry.get().strip()
        if not ofertante:
            messagebox.showwarning("Advertencia", "Debes ingresar el nombre del ofertante")
            return

        try:
            monto = float(self.monto_oferta_entry.get())
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número")
            return

        nueva_oferta = {
            'fecha': datetime.now(),
            'ofertante': ofertante,
            'monto': monto
        }

        self.valoraciones_collection.update_one(
            {'_id': ObjectId(self.selected_valoracion_id)},
            {'$push': {'historial_ofertas': nueva_oferta}}
        )

        messagebox.showinfo("Éxito", "Oferta agregada correctamente")

        # Recargar datos
        self.load_valoracion_data(self.selected_valoracion_id)
        self.load_valoraciones()

        # Limpiar campos de oferta
        self.ofertante_entry.delete(0, tk.END)
        self.monto_oferta_entry.delete(0, tk.END)

    def eliminar_oferta(self):
        """Elimina una oferta seleccionada"""
        selection = self.ofertas_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una oferta para eliminar")
            return

        if not self.selected_valoracion_id:
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta oferta?"):
            item = selection[0]
            values = self.ofertas_tree.item(item)['values']

            # Obtener la valoración actual
            valoracion = self.valoraciones_collection.find_one({'_id': ObjectId(self.selected_valoracion_id)})

            if valoracion and 'historial_ofertas' in valoracion:
                # Filtrar ofertas
                nuevas_ofertas = []
                for oferta in valoracion['historial_ofertas']:
                    fecha_str = oferta['fecha'].strftime("%d/%m/%Y %H:%M") if isinstance(oferta.get('fecha'), datetime) else "N/A"
                    if fecha_str != values[0] or oferta.get('ofertante') != values[1]:
                        nuevas_ofertas.append(oferta)

                # Actualizar
                self.valoraciones_collection.update_one(
                    {'_id': ObjectId(self.selected_valoracion_id)},
                    {'$set': {'historial_ofertas': nuevas_ofertas}}
                )

                messagebox.showinfo("Éxito", "Oferta eliminada correctamente")
                self.load_valoracion_data(self.selected_valoracion_id)
                self.load_valoraciones()

    def eliminar_valoracion(self):
        """Elimina una valoración completa"""
        if not self.selected_valoracion_id:
            messagebox.showwarning("Advertencia", "Selecciona una valoración para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta valoración y todas sus ofertas?"):
            self.valoraciones_collection.delete_one({'_id': ObjectId(self.selected_valoracion_id)})
            messagebox.showinfo("Éxito", "Valoración eliminada correctamente")

            self.load_valoraciones()
            self.limpiar_formulario()
            self.selected_valoracion_id = None

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.obra_combo.set('')
        self.valoracion_entry.delete(0, tk.END)
        self.moneda_combo.current(0)
        self.dia_val_entry.delete(0, tk.END)
        self.mes_val_entry.delete(0, tk.END)
        self.anio_val_entry.delete(0, tk.END)
        self.perito_entry.delete(0, tk.END)
        self.ofertante_entry.delete(0, tk.END)
        self.monto_oferta_entry.delete(0, tk.END)

        for item in self.ofertas_tree.get_children():
            self.ofertas_tree.delete(item)

        self.selected_valoracion_id = None
        self.current_obra_id = None
