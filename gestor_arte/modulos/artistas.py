"""
Módulo 1: Registro de Artistas
CRUD de perfiles de artistas, incluyendo biografía y enlaces
Actor: Curador
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

class ArtistasWindow:
    def __init__(self):
        """Inicializa la ventana de gestión de artistas"""
        self.window = tk.Toplevel()
        self.window.title("Registro de Artistas")
        self.window.geometry("1100x700")
        self.window.configure(bg=COLORS['bg_primary'])

        # Configurar estilos
        configure_styles()

        self.db = get_db()
        self.artistas_collection = self.db.get_collection('artistas')

        self.selected_artista_id = None

        self.setup_ui()
        self.load_artistas()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Header
        header_frame = tk.Frame(self.window, bg='#3498DB', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Título en el header
        title_label = tk.Label(
            header_frame,
            text="📝 REGISTRO DE ARTISTAS",
            font=('Segoe UI', 20, 'bold'),
            bg='#3498DB',
            fg=COLORS['text_light']
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=30)

        subtitle_label = tk.Label(
            header_frame,
            text="Gestión de perfiles de artistas con biografía y enlaces",
            font=('Segoe UI', 10),
            bg='#3498DB',
            fg=COLORS['text_light']
        )
        subtitle_label.pack(side=tk.LEFT, padx=(0, 30), pady=30)

        # Frame principal
        main_frame = tk.Frame(self.window, bg=COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel izquierdo - Lista de artistas
        left_panel = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Título del panel izquierdo
        left_title_frame = tk.Frame(left_panel, bg=COLORS['bg_secondary'], height=50)
        left_title_frame.pack(fill=tk.X, pady=(0, 5))
        left_title_frame.pack_propagate(False)

        tk.Label(
            left_title_frame,
            text="Lista de Artistas",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).pack(side=tk.LEFT, padx=15, pady=10)

        # Treeview con estilo
        tree_frame = tk.Frame(left_panel, bg=COLORS['bg_secondary'], relief='solid', borderwidth=1)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview
        columns = ("nombre", "pais", "fecha_nacimiento")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings", height=20)

        self.tree.heading("#0", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("pais", text="País")
        self.tree.heading("fecha_nacimiento", text="F. Nacimiento")

        self.tree.column("#0", width=50)
        self.tree.column("nombre", width=150)
        self.tree.column("pais", width=100)
        self.tree.column("fecha_nacimiento", width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind selección
        self.tree.bind('<<TreeviewSelect>>', self.on_select_artista)

        # Panel derecho - Formulario
        right_panel = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Título del panel derecho
        right_title_frame = tk.Frame(right_panel, bg=COLORS['bg_secondary'], height=50)
        right_title_frame.pack(fill=tk.X, pady=(0, 5))
        right_title_frame.pack_propagate(False)

        tk.Label(
            right_title_frame,
            text="Datos del Artista",
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

        # País
        tk.Label(
            form_content,
            text="País:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        self.pais_entry = tk.Entry(
            form_content,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.pais_entry.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15), ipady=8)
        row += 2

        # Fecha de nacimiento
        tk.Label(
            form_content,
            text="Fecha de Nacimiento:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        fecha_frame = tk.Frame(form_content, bg=COLORS['bg_secondary'])
        fecha_frame.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15))

        tk.Label(fecha_frame, text="Día:", bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT)
        self.dia_entry = tk.Entry(
            fecha_frame,
            width=5,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.dia_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(fecha_frame, text="Mes:", bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT, padx=(10, 0))
        self.mes_entry = tk.Entry(
            fecha_frame,
            width=5,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.mes_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(fecha_frame, text="Año:", bg=COLORS['bg_secondary'], fg=COLORS['text_primary']).pack(side=tk.LEFT, padx=(10, 0))
        self.anio_entry = tk.Entry(
            fecha_frame,
            width=8,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.anio_entry.pack(side=tk.LEFT, padx=2)
        row += 2

        # Biografía
        tk.Label(
            form_content,
            text="Biografía:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        self.biografia_text = scrolledtext.ScrolledText(
            form_content,
            width=40,
            height=6,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1
        )
        self.biografia_text.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15))
        row += 2

        # Enlaces
        tk.Label(
            form_content,
            text="Enlaces (uno por línea):",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        self.enlaces_text = scrolledtext.ScrolledText(
            form_content,
            width=40,
            height=4,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1
        )
        self.enlaces_text.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15))
        row += 2

        # Configurar expansión
        form_content.columnconfigure(0, weight=1)

        # Botones de acción
        buttons_frame = tk.Frame(form_content, bg=COLORS['bg_secondary'])
        buttons_frame.grid(row=row, column=0, sticky=tk.EW, pady=(10, 0))

        # Crear botones con estilos
        btn_config = [
            ("Nuevo", self.nuevo_artista, COLORS['accent']),
            ("Guardar", self.guardar_artista, COLORS['success']),
            ("Actualizar", self.actualizar_artista, COLORS['warning']),
            ("Eliminar", self.eliminar_artista, COLORS['danger']),
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

    def load_artistas(self):
        """Carga todos los artistas en el TreeView"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        artistas = self.artistas_collection.find().sort("nombre", 1)

        for idx, artista in enumerate(artistas, 1):
            fecha_nac = "N/A"
            if 'fecha_nacimiento' in artista and artista['fecha_nacimiento']:
                if isinstance(artista['fecha_nacimiento'], datetime):
                    fecha_nac = artista['fecha_nacimiento'].strftime("%d/%m/%Y")
                else:
                    fecha_nac = artista['fecha_nacimiento']

            self.tree.insert("", tk.END, iid=str(artista['_id']), text=str(idx),
                           values=(artista.get('nombre', ''),
                                 artista.get('pais', ''),
                                 fecha_nac))

    def on_select_artista(self, event):
        """Maneja la selección de un artista en el TreeView"""
        selection = self.tree.selection()
        if selection:
            artista_id = selection[0]
            self.selected_artista_id = artista_id
            self.load_artista_data(artista_id)

    def load_artista_data(self, artista_id):
        """Carga los datos de un artista en el formulario"""
        artista = self.artistas_collection.find_one({'_id': ObjectId(artista_id)})

        if artista:
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, artista.get('nombre', ''))

            self.pais_entry.delete(0, tk.END)
            self.pais_entry.insert(0, artista.get('pais', ''))

            # Fecha de nacimiento
            if 'fecha_nacimiento' in artista and artista['fecha_nacimiento']:
                if isinstance(artista['fecha_nacimiento'], datetime):
                    self.dia_entry.delete(0, tk.END)
                    self.dia_entry.insert(0, artista['fecha_nacimiento'].day)
                    self.mes_entry.delete(0, tk.END)
                    self.mes_entry.insert(0, artista['fecha_nacimiento'].month)
                    self.anio_entry.delete(0, tk.END)
                    self.anio_entry.insert(0, artista['fecha_nacimiento'].year)

            self.biografia_text.delete(1.0, tk.END)
            self.biografia_text.insert(1.0, artista.get('biografia', ''))

            self.enlaces_text.delete(1.0, tk.END)
            if 'enlaces' in artista and artista['enlaces']:
                enlaces_str = '\n'.join(artista['enlaces'])
                self.enlaces_text.insert(1.0, enlaces_str)

    def nuevo_artista(self):
        """Prepara el formulario para un nuevo artista"""
        self.limpiar_formulario()
        self.selected_artista_id = None

    def guardar_artista(self):
        """Guarda un nuevo artista"""
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio")
            return

        try:
            dia = int(self.dia_entry.get()) if self.dia_entry.get() else 1
            mes = int(self.mes_entry.get()) if self.mes_entry.get() else 1
            anio = int(self.anio_entry.get()) if self.anio_entry.get() else 2000
            fecha_nacimiento = datetime(anio, mes, dia)
        except ValueError:
            messagebox.showerror("Error", "Fecha de nacimiento inválida")
            return

        enlaces = [e.strip() for e in self.enlaces_text.get(1.0, tk.END).strip().split('\n') if e.strip()]

        artista_data = {
            'nombre': nombre,
            'pais': self.pais_entry.get().strip(),
            'fecha_nacimiento': fecha_nacimiento,
            'biografia': self.biografia_text.get(1.0, tk.END).strip(),
            'enlaces': enlaces
        }

        self.artistas_collection.insert_one(artista_data)
        messagebox.showinfo("Éxito", "Artista guardado correctamente")

        self.load_artistas()
        self.limpiar_formulario()

    def actualizar_artista(self):
        """Actualiza un artista existente"""
        if not self.selected_artista_id:
            messagebox.showwarning("Advertencia", "Selecciona un artista para actualizar")
            return

        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio")
            return

        try:
            dia = int(self.dia_entry.get()) if self.dia_entry.get() else 1
            mes = int(self.mes_entry.get()) if self.mes_entry.get() else 1
            anio = int(self.anio_entry.get()) if self.anio_entry.get() else 2000
            fecha_nacimiento = datetime(anio, mes, dia)
        except ValueError:
            messagebox.showerror("Error", "Fecha de nacimiento inválida")
            return

        enlaces = [e.strip() for e in self.enlaces_text.get(1.0, tk.END).strip().split('\n') if e.strip()]

        artista_data = {
            'nombre': nombre,
            'pais': self.pais_entry.get().strip(),
            'fecha_nacimiento': fecha_nacimiento,
            'biografia': self.biografia_text.get(1.0, tk.END).strip(),
            'enlaces': enlaces
        }

        self.artistas_collection.update_one(
            {'_id': ObjectId(self.selected_artista_id)},
            {'$set': artista_data}
        )

        messagebox.showinfo("Éxito", "Artista actualizado correctamente")
        self.load_artistas()

    def eliminar_artista(self):
        """Elimina un artista"""
        if not self.selected_artista_id:
            messagebox.showwarning("Advertencia", "Selecciona un artista para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este artista?"):
            self.artistas_collection.delete_one({'_id': ObjectId(self.selected_artista_id)})
            messagebox.showinfo("Éxito", "Artista eliminado correctamente")

            self.load_artistas()
            self.limpiar_formulario()
            self.selected_artista_id = None

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.nombre_entry.delete(0, tk.END)
        self.pais_entry.delete(0, tk.END)
        self.dia_entry.delete(0, tk.END)
        self.mes_entry.delete(0, tk.END)
        self.anio_entry.delete(0, tk.END)
        self.biografia_text.delete(1.0, tk.END)
        self.enlaces_text.delete(1.0, tk.END)
        self.selected_artista_id = None
