"""
Módulo 5: Búsqueda por Atributo
Interfaz de búsqueda flexible por cualquier atributo anidado en el documento de la obra
Actor: Usuario
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from database import get_db
from bson.objectid import ObjectId
import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import configure_styles, COLORS, FONTS

class BusquedaWindow:
    def __init__(self):
        """Inicializa la ventana de búsqueda"""
        self.window = tk.Toplevel()
        self.window.title("Búsqueda por Atributo")
        self.window.geometry("1400x800")
        self.window.configure(bg=COLORS['bg_primary'])

        # Configurar estilos
        configure_styles()

        self.db = get_db()
        self.obras_collection = self.db.get_collection('obras')
        self.artistas_collection = self.db.get_collection('artistas')

        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Header
        header_frame = tk.Frame(self.window, bg='#E74C3C', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Título en el header
        title_label = tk.Label(
            header_frame,
            text="🔍 BÚSQUEDA AVANZADA",
            font=('Segoe UI', 20, 'bold'),
            bg='#E74C3C',
            fg=COLORS['text_light']
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=30)

        subtitle_label = tk.Label(
            header_frame,
            text="Búsqueda flexible por cualquier atributo de las obras",
            font=('Segoe UI', 10),
            bg='#E74C3C',
            fg=COLORS['text_light']
        )
        subtitle_label.pack(side=tk.LEFT, padx=(0, 30), pady=30)

        # Frame principal
        main_frame = tk.Frame(self.window, bg=COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel superior - Criterios de búsqueda
        search_title_frame = tk.Frame(main_frame, bg=COLORS['bg_secondary'], height=50)
        search_title_frame.pack(fill=tk.X, pady=(0, 5))
        search_title_frame.pack_propagate(False)

        tk.Label(
            search_title_frame,
            text="Criterios de Búsqueda",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).pack(side=tk.LEFT, padx=15, pady=10)

        # Contenedor de búsqueda
        search_frame = tk.Frame(main_frame, bg=COLORS['bg_secondary'], relief='solid', borderwidth=1)
        search_frame.pack(fill=tk.X, pady=(0, 15))

        search_content = tk.Frame(search_frame, bg=COLORS['bg_secondary'])
        search_content.pack(fill=tk.X, padx=25, pady=20)

        # Búsqueda por texto
        text_frame = tk.Frame(search_content, bg=COLORS['bg_secondary'])
        text_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            text_frame,
            text="Búsqueda por Texto:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.texto_entry = tk.Entry(
            text_frame,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.texto_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 10))

        tk.Label(
            text_frame,
            text="(busca en título, descripción)",
            font=('Segoe UI', 9),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_secondary']
        ).pack(side=tk.LEFT)

        # Filtros específicos
        filters_frame = tk.Frame(search_content, bg=COLORS['bg_secondary'])
        filters_frame.pack(fill=tk.X, pady=(0, 15))

        # Primera fila: Artista y Técnica
        row1 = tk.Frame(filters_frame, bg=COLORS['bg_secondary'])
        row1.pack(fill=tk.X, pady=(0, 10))

        # Artista
        artista_col = tk.Frame(row1, bg=COLORS['bg_secondary'])
        artista_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(
            artista_col,
            text="Artista:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(0, 5))

        self.artista_combo = ttk.Combobox(artista_col, font=('Segoe UI', 10))
        self.artista_combo.pack(fill=tk.X, ipady=6)

        # Técnica
        tecnica_col = tk.Frame(row1, bg=COLORS['bg_secondary'])
        tecnica_col.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            tecnica_col,
            text="Técnica:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(0, 5))

        self.tecnica_combo = ttk.Combobox(
            tecnica_col,
            values=["Todas", "Pintura", "Escultura", "Fotografía", "Grabado", "Arte Digital", "Instalación"],
            font=('Segoe UI', 10)
        )
        self.tecnica_combo.current(0)
        self.tecnica_combo.pack(fill=tk.X, ipady=6)

        # Segunda fila: Rango de años
        row2 = tk.Frame(filters_frame, bg=COLORS['bg_secondary'])
        row2.pack(fill=tk.X)

        # Año desde
        desde_col = tk.Frame(row2, bg=COLORS['bg_secondary'])
        desde_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(
            desde_col,
            text="Año desde:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(0, 5))

        self.anio_desde_entry = tk.Entry(
            desde_col,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.anio_desde_entry.pack(fill=tk.X, ipady=6)

        # Año hasta
        hasta_col = tk.Frame(row2, bg=COLORS['bg_secondary'])
        hasta_col.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            hasta_col,
            text="Año hasta:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(0, 5))

        self.anio_hasta_entry = tk.Entry(
            hasta_col,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.anio_hasta_entry.pack(fill=tk.X, ipady=6)

        # Separador
        separator = tk.Frame(search_content, bg=COLORS['border'], height=2)
        separator.pack(fill=tk.X, pady=15)

        # Búsqueda avanzada en metadatos
        tk.Label(
            search_content,
            text="Búsqueda Avanzada en Metadatos:",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).pack(anchor=tk.W, pady=(0, 10))

        advanced_frame = tk.Frame(search_content, bg=COLORS['bg_secondary'])
        advanced_frame.pack(fill=tk.X, pady=(0, 10))

        # Campo
        campo_col = tk.Frame(advanced_frame, bg=COLORS['bg_secondary'])
        campo_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(
            campo_col,
            text="Campo:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(0, 5))

        self.campo_meta_entry = tk.Entry(
            campo_col,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.campo_meta_entry.pack(fill=tk.X, ipady=6)

        # Valor
        valor_col = tk.Frame(advanced_frame, bg=COLORS['bg_secondary'])
        valor_col.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            valor_col,
            text="Valor:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(0, 5))

        self.valor_meta_entry = tk.Entry(
            valor_col,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.valor_meta_entry.pack(fill=tk.X, ipady=6)

        tk.Label(
            search_content,
            text="(ej. Campo: pigmento, Valor: óleo)",
            font=('Segoe UI', 9),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_secondary']
        ).pack(anchor=tk.W)

        # Botones de búsqueda
        buttons_search_frame = tk.Frame(search_content, bg=COLORS['bg_secondary'])
        buttons_search_frame.pack(fill=tk.X, pady=(20, 0))

        btn_search_config = [
            ("Buscar", self.buscar, COLORS['accent']),
            ("Limpiar Búsqueda", self.limpiar_busqueda, COLORS['warning']),
            ("Mostrar Todas", self.mostrar_todas, COLORS['success'])
        ]

        for idx, (text, command, color) in enumerate(btn_search_config):
            btn = tk.Button(
                buttons_search_frame,
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
            btn.grid(row=0, column=idx, padx=5, sticky=tk.EW, ipady=10)
            buttons_search_frame.columnconfigure(idx, weight=1)

            # Efecto hover
            def make_hover(button, base_color):
                def on_enter(e):
                    button['bg'] = self.lighten_color(base_color)
                def on_leave(e):
                    button['bg'] = base_color
                button.bind("<Enter>", on_enter)
                button.bind("<Leave>", on_leave)

            make_hover(btn, color)

        # Panel de resultados
        results_title_frame = tk.Frame(main_frame, bg=COLORS['bg_secondary'], height=50)
        results_title_frame.pack(fill=tk.X, pady=(10, 5))
        results_title_frame.pack_propagate(False)

        tk.Label(
            results_title_frame,
            text="Resultados de la Búsqueda",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).pack(side=tk.LEFT, padx=15, pady=10)

        self.resultados_label = tk.Label(
            results_title_frame,
            text="Resultados: 0",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['accent']
        )
        self.resultados_label.pack(side=tk.RIGHT, padx=15, pady=10)

        # Contenedor de resultados
        results_container = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        results_container.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo - Lista de resultados
        left_panel = tk.Frame(results_container, bg=COLORS['bg_secondary'], relief='solid', borderwidth=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Treeview
        columns = ("titulo", "artista", "tecnica", "año")
        self.tree = ttk.Treeview(left_panel, columns=columns, show="tree headings", height=15)

        self.tree.heading("#0", text="ID")
        self.tree.heading("titulo", text="Título")
        self.tree.heading("artista", text="Artista")
        self.tree.heading("tecnica", text="Técnica")
        self.tree.heading("año", text="Año")

        self.tree.column("#0", width=40)
        self.tree.column("titulo", width=250)
        self.tree.column("artista", width=150)
        self.tree.column("tecnica", width=100)
        self.tree.column("año", width=80)

        scrollbar = ttk.Scrollbar(left_panel, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<<TreeviewSelect>>', self.on_select_obra)

        # Panel derecho - Detalles de la obra
        right_panel = tk.Frame(results_container, bg=COLORS['bg_secondary'], relief='solid', borderwidth=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Título panel detalles
        detalles_header = tk.Frame(right_panel, bg=COLORS['primary'], height=40)
        detalles_header.pack(fill=tk.X)
        detalles_header.pack_propagate(False)

        tk.Label(
            detalles_header,
            text="Detalles de la Obra",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['primary'],
            fg=COLORS['text_light']
        ).pack(side=tk.LEFT, padx=15, pady=10)

        # ScrolledText para detalles
        self.detalles_text = scrolledtext.ScrolledText(
            right_panel,
            width=50,
            height=30,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=('Segoe UI', 10),
            relief='flat',
            bg=COLORS['bg_secondary']
        )
        self.detalles_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Cargar artistas
        self.load_artistas()

    def lighten_color(self, color):
        """Aclara un color hexadecimal"""
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'

    def load_artistas(self):
        """Carga los artistas en el ComboBox"""
        artistas = self.artistas_collection.find().sort("nombre", 1)
        artistas_list = ["Todos"]

        for artista in artistas:
            artistas_list.append(artista['nombre'])

        self.artista_combo['values'] = artistas_list
        self.artista_combo.current(0)

    def buscar(self):
        """Realiza la búsqueda según los criterios especificados"""
        # Construir query
        query = {}

        # Búsqueda por texto
        texto = self.texto_entry.get().strip()
        if texto:
            query['$or'] = [
                {'titulo': {'$regex': texto, '$options': 'i'}},
                {'descripcion': {'$regex': texto, '$options': 'i'}}
            ]

        # Filtro por artista
        artista = self.artista_combo.get()
        if artista and artista != "Todos":
            artista_doc = self.artistas_collection.find_one({'nombre': artista})
            if artista_doc:
                query['artista_id'] = str(artista_doc['_id'])

        # Filtro por técnica
        tecnica = self.tecnica_combo.get()
        if tecnica and tecnica != "Todas":
            query['tecnica'] = tecnica

        # Filtro por rango de años
        anio_desde = self.anio_desde_entry.get().strip()
        anio_hasta = self.anio_hasta_entry.get().strip()

        if anio_desde or anio_hasta:
            anio_query = {}
            if anio_desde:
                try:
                    anio_query['$gte'] = int(anio_desde)
                except ValueError:
                    messagebox.showerror("Error", "Año desde debe ser un número")
                    return

            if anio_hasta:
                try:
                    anio_query['$lte'] = int(anio_hasta)
                except ValueError:
                    messagebox.showerror("Error", "Año hasta debe ser un número")
                    return

            if anio_query:
                query['anio'] = anio_query

        # Búsqueda en metadatos
        campo_meta = self.campo_meta_entry.get().strip()
        valor_meta = self.valor_meta_entry.get().strip()

        if campo_meta and valor_meta:
            meta_key = f'metadatos.{campo_meta}'
            query[meta_key] = {'$regex': valor_meta, '$options': 'i'}

        # Ejecutar búsqueda
        resultados = list(self.obras_collection.find(query))

        # Mostrar resultados
        self.mostrar_resultados(resultados)

    def mostrar_resultados(self, resultados):
        """Muestra los resultados de la búsqueda en el TreeView"""
        # Limpiar TreeView
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Actualizar contador
        self.resultados_label.config(text=f"Resultados: {len(resultados)}")

        # Insertar resultados
        for idx, obra in enumerate(resultados, 1):
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
            self.mostrar_detalles(obra_id)

    def mostrar_detalles(self, obra_id):
        """Muestra los detalles completos de una obra"""
        obra = self.obras_collection.find_one({'_id': ObjectId(obra_id)})

        if obra:
            # Habilitar edición temporalmente
            self.detalles_text.config(state=tk.NORMAL)
            self.detalles_text.delete(1.0, tk.END)

            # Construir texto de detalles
            detalles = f"═══════════════════════════════════════\n"
            detalles += f"DETALLES DE LA OBRA\n"
            detalles += f"═══════════════════════════════════════\n\n"

            detalles += f"Título: {obra.get('titulo', 'N/A')}\n\n"

            # Artista
            artista_nombre = "Desconocido"
            if 'artista_id' in obra:
                artista = self.artistas_collection.find_one({'_id': ObjectId(obra['artista_id'])})
                if artista:
                    artista_nombre = artista['nombre']
                    detalles += f"Artista: {artista_nombre}\n"
                    if 'pais' in artista:
                        detalles += f"País: {artista.get('pais', 'N/A')}\n"

            detalles += f"\nTécnica: {obra.get('tecnica', 'N/A')}\n"
            detalles += f"Año: {obra.get('anio', 'N/A')}\n\n"

            # Descripción
            if 'descripcion' in obra and obra['descripcion']:
                detalles += f"Descripción:\n{obra['descripcion']}\n\n"

            # Metadatos
            if 'metadatos' in obra and obra['metadatos']:
                detalles += f"───────────────────────────────────────\n"
                detalles += f"METADATOS ESPECÍFICOS\n"
                detalles += f"───────────────────────────────────────\n\n"

                for key, value in obra['metadatos'].items():
                    detalles += f"{key.capitalize()}: {value}\n"

            # Buscar valoración
            valoracion = self.db.get_collection('valoraciones').find_one({'obra_id': str(obra['_id'])})
            if valoracion:
                detalles += f"\n───────────────────────────────────────\n"
                detalles += f"VALORACIÓN\n"
                detalles += f"───────────────────────────────────────\n\n"
                detalles += f"Valor: ${valoracion.get('valoracion_actual', 0)} {valoracion.get('moneda', 'USD')}\n"

                if 'perito' in valoracion and valoracion['perito']:
                    detalles += f"Perito: {valoracion['perito']}\n"

                if 'historial_ofertas' in valoracion and valoracion['historial_ofertas']:
                    detalles += f"\nOfertas de subasta: {len(valoracion['historial_ofertas'])}\n"

                    if valoracion['historial_ofertas']:
                        max_oferta = max(valoracion['historial_ofertas'], key=lambda x: x.get('monto', 0))
                        detalles += f"Oferta más alta: ${max_oferta.get('monto', 0)} por {max_oferta.get('ofertante', 'N/A')}\n"

            # Buscar exposiciones
            exposiciones = list(self.db.get_collection('exposiciones').find({'obras': ObjectId(obra_id)}))
            if exposiciones:
                detalles += f"\n───────────────────────────────────────\n"
                detalles += f"EXPOSICIONES\n"
                detalles += f"───────────────────────────────────────\n\n"

                for expo in exposiciones:
                    detalles += f"• {expo.get('nombre', 'N/A')} ({expo.get('tema', 'N/A')})\n"

            self.detalles_text.insert(1.0, detalles)
            self.detalles_text.config(state=tk.DISABLED)

    def mostrar_todas(self):
        """Muestra todas las obras"""
        obras = list(self.obras_collection.find().sort("titulo", 1))
        self.mostrar_resultados(obras)

    def limpiar_busqueda(self):
        """Limpia todos los campos de búsqueda"""
        self.texto_entry.delete(0, tk.END)
        self.artista_combo.current(0)
        self.tecnica_combo.current(0)
        self.anio_desde_entry.delete(0, tk.END)
        self.anio_hasta_entry.delete(0, tk.END)
        self.campo_meta_entry.delete(0, tk.END)
        self.valor_meta_entry.delete(0, tk.END)

        # Limpiar resultados
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.detalles_text.config(state=tk.NORMAL)
        self.detalles_text.delete(1.0, tk.END)
        self.detalles_text.config(state=tk.DISABLED)

        self.resultados_label.config(text="Resultados: 0")
