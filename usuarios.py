"""
Módulo 6: Gestión de Usuarios
CRUD de usuarios del sistema con asignación de roles
Actor: Administrador
"""
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_db
from auth import AuthManager
from bson.objectid import ObjectId
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import configure_styles, COLORS, FONTS

class UsuariosWindow:
    def __init__(self):
        """Inicializa la ventana de gestión de usuarios"""
        self.window = tk.Toplevel()
        self.window.title("Gestión de Usuarios")
        self.window.geometry("1100x700")
        self.window.configure(bg=COLORS['bg_primary'])

        # Configurar estilos
        configure_styles()

        self.db = get_db()
        self.usuarios_collection = self.db.get_collection('usuarios')
        self.auth_manager = AuthManager()

        self.selected_usuario_id = None

        self.setup_ui()
        self.load_usuarios()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Header
        header_frame = tk.Frame(self.window, bg='#34495E', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Título en el header
        title_label = tk.Label(
            header_frame,
            text="👥 GESTIÓN DE USUARIOS",
            font=('Segoe UI', 20, 'bold'),
            bg='#34495E',
            fg=COLORS['text_light']
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=30)

        subtitle_label = tk.Label(
            header_frame,
            text="Administración de usuarios y roles del sistema",
            font=('Segoe UI', 10),
            bg='#34495E',
            fg=COLORS['accent_light']
        )
        subtitle_label.pack(side=tk.LEFT, padx=(0, 30), pady=30)

        # Frame principal
        main_frame = tk.Frame(self.window, bg=COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel izquierdo - Lista de usuarios
        left_panel = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Título del panel izquierdo
        left_title_frame = tk.Frame(left_panel, bg=COLORS['bg_secondary'], height=50)
        left_title_frame.pack(fill=tk.X, pady=(0, 5))
        left_title_frame.pack_propagate(False)

        tk.Label(
            left_title_frame,
            text="Lista de Usuarios",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        ).pack(side=tk.LEFT, padx=15, pady=10)

        # Treeview con estilo
        tree_frame = tk.Frame(left_panel, bg=COLORS['bg_secondary'], relief='solid', borderwidth=1)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview
        columns = ("username", "rol")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings", height=20)

        self.tree.heading("#0", text="ID")
        self.tree.heading("username", text="Usuario")
        self.tree.heading("rol", text="Rol")

        self.tree.column("#0", width=50)
        self.tree.column("username", width=200)
        self.tree.column("rol", width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind selección
        self.tree.bind('<<TreeviewSelect>>', self.on_select_usuario)

        # Panel derecho - Formulario
        right_panel = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Título del panel derecho
        right_title_frame = tk.Frame(right_panel, bg=COLORS['bg_secondary'], height=50)
        right_title_frame.pack(fill=tk.X, pady=(0, 5))
        right_title_frame.pack_propagate(False)

        tk.Label(
            right_title_frame,
            text="Datos del Usuario",
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

        # Usuario
        tk.Label(
            form_content,
            text="Nombre de Usuario:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(10, 5))

        self.username_entry = tk.Entry(
            form_content,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.username_entry.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15), ipady=8)
        row += 2

        # Contraseña
        tk.Label(
            form_content,
            text="Contraseña:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        self.password_entry = tk.Entry(
            form_content,
            font=('Segoe UI', 11),
            show="●",
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.password_entry.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15), ipady=8)
        row += 2

        # Confirmar contraseña
        tk.Label(
            form_content,
            text="Confirmar Contraseña:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        self.confirm_password_entry = tk.Entry(
            form_content,
            font=('Segoe UI', 11),
            show="●",
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.confirm_password_entry.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 15), ipady=8)
        row += 2

        # Rol
        tk.Label(
            form_content,
            text="Rol del Usuario:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        ).grid(row=row, column=0, sticky=tk.W, pady=(5, 5))

        self.rol_combo = ttk.Combobox(
            form_content,
            values=["Curador", "Administrador", "Usuario"],
            state="readonly",
            font=('Segoe UI', 10)
        )
        self.rol_combo.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, 20), ipady=8)
        row += 2

        # Separador
        separator = tk.Frame(form_content, bg=COLORS['border'], height=2)
        separator.grid(row=row, column=0, sticky=tk.EW, pady=15)
        row += 1

        # Información de permisos
        permisos_title = tk.Label(
            form_content,
            text="ℹ️ Permisos por Rol",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        )
        permisos_title.grid(row=row, column=0, sticky=tk.W, pady=(0, 10))
        row += 1

        permisos_info = tk.Text(
            form_content,
            font=('Segoe UI', 9),
            bg='#F8F9FA',
            fg=COLORS['text_primary'],
            relief='solid',
            borderwidth=1,
            height=6,
            wrap=tk.WORD
        )
        permisos_info.grid(row=row, column=0, sticky=tk.EW, pady=(0, 20))

        permisos_text = """📚 Curador:
   • Registro de Artistas  • Catálogo de Obras

⚙️ Administrador:
   • Exposiciones  • Valoraciones y Subastas  • Gestión de Usuarios

👤 Usuario:
   • Búsqueda por Atributo"""

        permisos_info.insert(1.0, permisos_text)
        permisos_info.config(state=tk.DISABLED)
        row += 1

        # Configurar expansión
        form_content.columnconfigure(0, weight=1)

        # Botones de acción
        buttons_frame = tk.Frame(form_content, bg=COLORS['bg_secondary'])
        buttons_frame.grid(row=row, column=0, sticky=tk.EW, pady=(10, 0))

        # Crear botones con estilos
        btn_config = [
            ("Nuevo", self.nuevo_usuario, COLORS['accent']),
            ("Guardar", self.guardar_usuario, COLORS['success']),
            ("Actualizar", self.actualizar_usuario, COLORS['warning']),
            ("Eliminar", self.eliminar_usuario, COLORS['danger']),
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

    def load_usuarios(self):
        """Carga todos los usuarios en el TreeView"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        usuarios = self.usuarios_collection.find().sort("username", 1)

        for idx, usuario in enumerate(usuarios, 1):
            self.tree.insert("", tk.END, iid=str(usuario['_id']), text=str(idx),
                           values=(usuario.get('username', ''),
                                 usuario.get('rol', '')))

    def on_select_usuario(self, event):
        """Maneja la selección de un usuario en el TreeView"""
        selection = self.tree.selection()
        if selection:
            usuario_id = selection[0]
            self.selected_usuario_id = usuario_id
            self.load_usuario_data(usuario_id)

    def load_usuario_data(self, usuario_id):
        """Carga los datos de un usuario en el formulario"""
        usuario = self.usuarios_collection.find_one({'_id': ObjectId(usuario_id)})

        if usuario:
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, usuario.get('username', ''))

            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)

            rol = usuario.get('rol', '')
            if rol in ["Curador", "Administrador", "Usuario"]:
                self.rol_combo.set(rol)

    def nuevo_usuario(self):
        """Prepara el formulario para un nuevo usuario"""
        self.limpiar_formulario()
        self.selected_usuario_id = None

    def guardar_usuario(self):
        """Guarda un nuevo usuario"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        rol = self.rol_combo.get()

        if not username:
            messagebox.showwarning("Advertencia", "El nombre de usuario es obligatorio")
            return

        if not password:
            messagebox.showwarning("Advertencia", "La contraseña es obligatoria")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        if len(password) < 6:
            messagebox.showwarning("Advertencia", "La contraseña debe tener al menos 6 caracteres")
            return

        if not rol:
            messagebox.showwarning("Advertencia", "Debes seleccionar un rol")
            return

        if self.usuarios_collection.find_one({'username': username}):
            messagebox.showerror("Error", "Este nombre de usuario ya existe")
            return

        success = self.auth_manager.create_user(username, password, rol)

        if success:
            messagebox.showinfo("Éxito", f"Usuario '{username}' creado correctamente")
            self.load_usuarios()
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario")

    def actualizar_usuario(self):
        """Actualiza un usuario existente"""
        if not self.selected_usuario_id:
            messagebox.showwarning("Advertencia", "Selecciona un usuario para actualizar")
            return

        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        rol = self.rol_combo.get()

        if not username:
            messagebox.showwarning("Advertencia", "El nombre de usuario es obligatorio")
            return

        if not rol:
            messagebox.showwarning("Advertencia", "Debes seleccionar un rol")
            return

        update_data = {
            'username': username,
            'rol': rol
        }

        if password:
            if password != confirm_password:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return

            if len(password) < 6:
                messagebox.showwarning("Advertencia", "La contraseña debe tener al menos 6 caracteres")
                return

            update_data['password'] = self.auth_manager.hash_password(password)

        self.usuarios_collection.update_one(
            {'_id': ObjectId(self.selected_usuario_id)},
            {'$set': update_data}
        )

        messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
        self.load_usuarios()

    def eliminar_usuario(self):
        """Elimina un usuario"""
        if not self.selected_usuario_id:
            messagebox.showwarning("Advertencia", "Selecciona un usuario para eliminar")
            return

        usuario = self.usuarios_collection.find_one({'_id': ObjectId(self.selected_usuario_id)})

        if usuario:
            if messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar al usuario '{usuario['username']}'?"):
                self.usuarios_collection.delete_one({'_id': ObjectId(self.selected_usuario_id)})
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")

                self.load_usuarios()
                self.limpiar_formulario()
                self.selected_usuario_id = None

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)
        self.rol_combo.set('')
        self.selected_usuario_id = None
