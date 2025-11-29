"""
Aplicación principal - Gestor de Perfiles de Arte y Artistas
Versión mejorada con autoconfiguración de base de datos
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Imports del sistema
from auth import AuthManager
from modulos import artistas, obras, exposiciones, subastas, busqueda, usuarios
from styles import configure_styles, COLORS, FONTS

# Imports de base de datos para la autoconfiguración
from database import get_db
from init_db import init_database

def verificar_y_configurar_db():
    """
    Verifica si existen datos al inicio. 
    Si la BD está vacía, ejecuta la inicialización y notifica al usuario.
    """
    # Creamos una ventana oculta temporal para poder mostrar alertas
    # antes de que arranque la aplicación principal
    temp_root = tk.Tk()
    temp_root.withdraw() 

    try:
        db = get_db()
        # Verificar conexión real (ping)
        db.client.admin.command('ping')
        
        coleccion_usuarios = db.get_collection('usuarios')
        
        # Si no hay usuarios, asumimos que la BD está nueva/vacía
        if coleccion_usuarios.count_documents({}) == 0:
            messagebox.showinfo(
                "Configuración Inicial", 
                "⚠️ La base de datos está vacía.\n\nEl sistema cargará automáticamente los datos de prueba y los usuarios iniciales."
            )
            
            # Ejecutamos el script de init_db
            init_database()
            
            messagebox.showinfo(
                "Inicialización Exitosa", 
                "✅ Se han creado los datos correctamente.\n\nPuedes ingresar con:\nUsuario: admin\nContraseña: admin123"
            )
            
    except Exception as e:
        messagebox.showerror(
            "Error Crítico", 
            f"❌ No se pudo conectar a MongoDB o inicializar los datos.\n\nAsegúrate de que MongoDB esté corriendo.\nError: {e}"
        )
        sys.exit(1)
    finally:
        # Destruimos la ventana temporal para limpiar memoria
        temp_root.destroy()

class LoginWindow:
    def __init__(self):
        """Inicializa la ventana de login"""
        self.root = tk.Tk()
        self.root.title("Gestor de Arte - Login")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS['primary'])

        # Configurar estilos
        configure_styles()

        self.auth_manager = AuthManager()
        self.current_user = None

        self.setup_ui()
        self.center_window()

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Configura la interfaz de usuario del login"""
        # Header con gradiente
        header_frame = tk.Frame(self.root, bg=COLORS['primary'], height=150)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Título principal
        title_label = tk.Label(
            header_frame,
            text="🎨 GESTOR DE ARTE",
            font=('Segoe UI', 28, 'bold'),
            bg=COLORS['primary'],
            fg=COLORS['text_light']
        )
        title_label.pack(pady=(30, 5))

        subtitle_label = tk.Label(
            header_frame,
            text="Sistema de Gestión de Perfiles de Arte y Artistas",
            font=('Segoe UI', 11),
            bg=COLORS['primary'],
            fg=COLORS['accent_light']
        )
        subtitle_label.pack()

        # Frame principal con fondo claro
        main_frame = tk.Frame(self.root, bg=COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # Card de login
        login_card = tk.Frame(main_frame, bg=COLORS['bg_secondary'], relief='raised', borderwidth=2)
        login_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título del formulario
        form_title = tk.Label(
            login_card,
            text="Iniciar Sesión",
            font=('Segoe UI', 16, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['primary']
        )
        form_title.pack(pady=(20, 10))

        # Frame para campos
        fields_frame = tk.Frame(login_card, bg=COLORS['bg_secondary'])
        fields_frame.pack(pady=20, padx=30, fill=tk.X)

        # Usuario
        user_label = tk.Label(
            fields_frame,
            text="Usuario:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        )
        user_label.pack(anchor=tk.W, pady=(10, 5))

        self.username_entry = tk.Entry(
            fields_frame,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.username_entry.pack(fill=tk.X, ipady=8)

        # Contraseña
        pass_label = tk.Label(
            fields_frame,
            text="Contraseña:",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        )
        pass_label.pack(anchor=tk.W, pady=(15, 5))

        self.password_entry = tk.Entry(
            fields_frame,
            font=('Segoe UI', 11),
            show="●",
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['accent']
        )
        self.password_entry.pack(fill=tk.X, ipady=8)

        # Botón de login
        login_button = tk.Button(
            fields_frame,
            text="INICIAR SESIÓN",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['accent'],
            fg=COLORS['text_light'],
            activebackground=COLORS['accent_light'],
            activeforeground=COLORS['text_light'],
            relief='flat',
            cursor='hand2',
            command=self.login
        )
        login_button.pack(fill=tk.X, pady=(25, 10), ipady=12)

        # Efecto hover para el botón
        def on_enter(e):
            login_button['background'] = COLORS['accent_light']

        def on_leave(e):
            login_button['background'] = COLORS['accent']

        login_button.bind("<Enter>", on_enter)
        login_button.bind("<Leave>", on_leave)

        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.login())

        # Información de usuarios de prueba
        info_frame = tk.Frame(login_card, bg=COLORS['bg_secondary'])
        info_frame.pack(pady=(10, 20), padx=30, fill=tk.X)

        info_title = tk.Label(
            info_frame,
            text="Usuarios de Prueba:",
            font=('Segoe UI', 9, 'bold'),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_secondary']
        )
        info_title.pack(anchor=tk.W)

        usuarios_info = [
            ("👤 curador / curador123", "Rol: Curador"),
            ("👤 admin / admin123", "Rol: Administrador"),
            ("👤 usuario / usuario123", "Rol: Usuario")
        ]

        for user_text, rol_text in usuarios_info:
            user_frame = tk.Frame(info_frame, bg=COLORS['bg_secondary'])
            user_frame.pack(fill=tk.X, pady=2)

            tk.Label(
                user_frame,
                text=user_text,
                font=('Segoe UI', 8),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_primary']
            ).pack(side=tk.LEFT)

            tk.Label(
                user_frame,
                text=rol_text,
                font=('Segoe UI', 8, 'italic'),
                bg=COLORS['bg_secondary'],
                fg=COLORS['accent']
            ).pack(side=tk.RIGHT)

    def login(self):
        """Procesa el login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Advertencia", "Por favor ingresa usuario y contraseña")
            return

        user = self.auth_manager.authenticate(username, password)

        if user:
            self.current_user = user
            self.root.destroy()
            self.open_main_menu()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            self.password_entry.delete(0, tk.END)
            # Efecto de shake (simulado)
            self.username_entry.configure(highlightbackground=COLORS['danger'])
            self.password_entry.configure(highlightbackground=COLORS['danger'])
            self.root.after(1000, lambda: [
                self.username_entry.configure(highlightbackground=COLORS['border']),
                self.password_entry.configure(highlightbackground=COLORS['border'])
            ])

    def open_main_menu(self):
        """Abre el menú principal"""
        MainMenu(self.current_user)

    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()


class MainMenu:
    def __init__(self, user):
        """
        Inicializa el menú principal

        Args:
            user: Diccionario con información del usuario
        """
        self.root = tk.Tk()
        self.root.title("Gestor de Arte - Menú Principal")
        self.root.geometry("900x700")
        self.root.configure(bg=COLORS['bg_primary'])

        # Configurar estilos
        configure_styles()

        self.user = user
        self.permissions = AuthManager().get_user_permissions(user['rol'])

        self.setup_ui()
        self.center_window()
        self.root.mainloop()

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Configura la interfaz del menú principal"""
        # Header
        header_frame = tk.Frame(self.root, bg=COLORS['primary'], height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Contenedor del header
        header_content = tk.Frame(header_frame, bg=COLORS['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30)

        # Título
        title_label = tk.Label(
            header_content,
            text="🎨 GESTOR DE ARTE",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['primary'],
            fg=COLORS['text_light']
        )
        title_label.pack(side=tk.LEFT, pady=20)

        # Info del usuario (derecha)
        user_info_frame = tk.Frame(header_content, bg=COLORS['primary'])
        user_info_frame.pack(side=tk.RIGHT, pady=20)

        welcome_label = tk.Label(
            user_info_frame,
            text=f"Bienvenido, {self.user['username']}",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['primary'],
            fg=COLORS['text_light']
        )
        welcome_label.pack(anchor=tk.E)

        # Icono de rol basado en el tipo
        rol_icons = {
            'Curador': '📚',
            'Administrador': '⚙️',
            'Usuario': '👤'
        }
        icon = rol_icons.get(self.user['rol'], '👤')

        rol_label = tk.Label(
            user_info_frame,
            text=f"{icon} {self.user['rol']}",
            font=('Segoe UI', 10),
            bg=COLORS['primary'],
            fg=COLORS['accent_light']
        )
        rol_label.pack(anchor=tk.E)

        # Frame principal
        main_frame = tk.Frame(self.root, bg=COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # Título de módulos
        modules_title = tk.Label(
            main_frame,
            text="Módulos Disponibles",
            font=('Segoe UI', 18, 'bold'),
            bg=COLORS['bg_primary'],
            fg=COLORS['primary']
        )
        modules_title.pack(pady=(0, 20))

        # Container para las tarjetas de módulos
        modules_container = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        modules_container.pack(fill=tk.BOTH, expand=True)

        # Definición de módulos con iconos
        all_modules = {
            'artistas': {
                'name': '📝 Registro de Artistas',
                'description': 'Gestión completa de perfiles de artistas',
                'color': '#3498DB',
                'function': self.open_artistas
            },
            'obras': {
                'name': '🎨 Catálogo de Obras',
                'description': 'Administración de obras de arte',
                'color': '#9B59B6',
                'function': self.open_obras
            },
            'exposiciones': {
                'name': '🏛️ Exposiciones',
                'description': 'Creación y gestión de exposiciones',
                'color': '#E67E22',
                'function': self.open_exposiciones
            },
            'subastas': {
                'name': '💰 Valoraciones y Subastas',
                'description': 'Sistema de valoración y subastas',
                'color': '#27AE60',
                'function': self.open_subastas
            },
            'busqueda': {
                'name': '🔍 Búsqueda Avanzada',
                'description': 'Búsqueda flexible por atributos',
                'color': '#E74C3C',
                'function': self.open_busqueda
            },
            'usuarios': {
                'name': '👥 Gestión de Usuarios',
                'description': 'Administración de usuarios del sistema',
                'color': '#34495E',
                'function': self.open_usuarios
            }
        }

        # Crear tarjetas para módulos permitidos
        row = 0
        col = 0
        for module_id in self.permissions:
            if module_id in all_modules:
                module = all_modules[module_id]

                # Tarjeta de módulo
                card = tk.Frame(
                    modules_container,
                    bg=COLORS['bg_secondary'],
                    relief='raised',
                    borderwidth=2,
                    cursor='hand2'
                )
                card.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')

                # Barra de color superior
                color_bar = tk.Frame(card, bg=module['color'], height=8)
                color_bar.pack(fill=tk.X)

                # Contenido de la tarjeta
                content_frame = tk.Frame(card, bg=COLORS['bg_secondary'])
                content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

                # Nombre del módulo
                name_label = tk.Label(
                    content_frame,
                    text=module['name'],
                    font=('Segoe UI', 14, 'bold'),
                    bg=COLORS['bg_secondary'],
                    fg=COLORS['primary']
                )
                name_label.pack(pady=(0, 10))

                # Descripción
                desc_label = tk.Label(
                    content_frame,
                    text=module['description'],
                    font=('Segoe UI', 9),
                    bg=COLORS['bg_secondary'],
                    fg=COLORS['text_secondary'],
                    wraplength=200
                )
                desc_label.pack(pady=(0, 15))

                # Botón de abrir
                open_button = tk.Button(
                    content_frame,
                    text="ABRIR MÓDULO",
                    font=('Segoe UI', 10, 'bold'),
                    bg=module['color'],
                    fg=COLORS['text_light'],
                    activebackground=module['color'],
                    activeforeground=COLORS['text_light'],
                    relief='flat',
                    cursor='hand2',
                    command=module['function']
                )
                open_button.pack(fill=tk.X, ipady=8)

                # Efecto hover para la tarjeta
                def make_hover_effect(widget, enter_bg, leave_bg):
                    def on_enter(e):
                        widget['bg'] = enter_bg

                    def on_leave(e):
                        widget['bg'] = leave_bg

                    widget.bind("<Enter>", on_enter)
                    widget.bind("<Leave>", on_leave)

                make_hover_effect(card, COLORS['border_light'], COLORS['bg_secondary'])

                # Click en toda la tarjeta
                def make_card_click(func):
                    return lambda e: func()

                card.bind("<Button-1>", make_card_click(module['function']))

                # Siguiente posición
                col += 1
                if col > 1:  # 2 columnas
                    col = 0
                    row += 1

        # Configurar grid
        for i in range(2):
            modules_container.columnconfigure(i, weight=1)

        # Botón de cerrar sesión
        logout_frame = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        logout_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))

        logout_button = tk.Button(
            logout_frame,
            text="🚪 CERRAR SESIÓN",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['danger'],
            fg=COLORS['text_light'],
            activebackground='#EC7063',
            activeforeground=COLORS['text_light'],
            relief='flat',
            cursor='hand2',
            command=self.logout
        )
        logout_button.pack(ipadx=30, ipady=10)

        # Efecto hover
        def on_enter(e):
            logout_button['background'] = '#EC7063'

        def on_leave(e):
            logout_button['background'] = COLORS['danger']

        logout_button.bind("<Enter>", on_enter)
        logout_button.bind("<Leave>", on_leave)

    def open_artistas(self):
        """Abre el módulo de artistas"""
        artistas.ArtistasWindow()

    def open_obras(self):
        """Abre el módulo de obras"""
        obras.ObrasWindow()

    def open_exposiciones(self):
        """Abre el módulo de exposiciones"""
        exposiciones.ExposicionesWindow()

    def open_subastas(self):
        """Abre el módulo de subastas"""
        subastas.SubastasWindow()

    def open_busqueda(self):
        """Abre el módulo de búsqueda"""
        busqueda.BusquedaWindow()

    def open_usuarios(self):
        """Abre el módulo de gestión de usuarios"""
        usuarios.UsuariosWindow()

    def logout(self):
        """Cierra sesión y vuelve al login"""
        self.root.destroy()
        app = LoginWindow()
        app.run()


if __name__ == "__main__":
    # PASO 1: Verificar y configurar la Base de Datos Automáticamente
    verificar_y_configurar_db()
    
    # PASO 2: Iniciar la Aplicación
    app = LoginWindow()
    app.run()