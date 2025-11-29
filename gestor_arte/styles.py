"""
Estilos y configuración visual para la aplicación
Define colores, fuentes y estilos consistentes
"""
from tkinter import ttk

# Paleta de colores
COLORS = {
    # Colores principales
    'primary': '#2C3E50',          # Azul oscuro elegante
    'primary_light': '#34495E',    # Azul oscuro claro
    'primary_dark': '#1A252F',     # Azul muy oscuro

    # Colores secundarios
    'secondary': '#E74C3C',        # Rojo coral
    'secondary_light': '#EC7063',  # Rojo coral claro

    # Colores de acento
    'accent': '#3498DB',           # Azul brillante
    'accent_light': '#5DADE2',     # Azul brillante claro
    'accent_dark': '#2874A6',      # Azul brillante oscuro

    # Colores de éxito/error
    'success': '#27AE60',          # Verde
    'warning': '#F39C12',          # Naranja
    'danger': '#E74C3C',           # Rojo
    'info': '#3498DB',             # Azul

    # Colores de fondo
    'bg_primary': '#ECF0F1',       # Gris muy claro
    'bg_secondary': '#FFFFFF',     # Blanco
    'bg_dark': '#2C3E50',          # Oscuro
    'bg_card': '#FFFFFF',          # Blanco para tarjetas

    # Colores de texto
    'text_primary': '#2C3E50',     # Texto oscuro
    'text_secondary': '#7F8C8D',   # Texto gris
    'text_light': '#FFFFFF',       # Texto blanco

    # Colores de bordes
    'border': '#BDC3C7',           # Gris claro
    'border_light': '#ECF0F1',     # Gris muy claro
}

# Fuentes
FONTS = {
    'title': ('Segoe UI', 24, 'bold'),
    'heading': ('Segoe UI', 16, 'bold'),
    'subheading': ('Segoe UI', 12, 'bold'),
    'body': ('Segoe UI', 10),
    'small': ('Segoe UI', 9),
    'button': ('Segoe UI', 10, 'bold'),
}

def configure_styles():
    """Configura los estilos ttk para la aplicación"""
    style = ttk.Style()

    # Intentar usar un tema base moderno
    try:
        style.theme_use('clam')
    except:
        pass

    # Estilo para Frame
    style.configure('TFrame', background=COLORS['bg_primary'])
    style.configure('Card.TFrame', background=COLORS['bg_card'], relief='raised', borderwidth=1)

    # Estilo para LabelFrame
    style.configure('TLabelframe',
                   background=COLORS['bg_primary'],
                   foreground=COLORS['text_primary'],
                   borderwidth=2,
                   relief='groove')
    style.configure('TLabelframe.Label',
                   background=COLORS['bg_primary'],
                   foreground=COLORS['primary'],
                   font=FONTS['subheading'])

    # Estilo para Label
    style.configure('TLabel',
                   background=COLORS['bg_primary'],
                   foreground=COLORS['text_primary'],
                   font=FONTS['body'])

    style.configure('Title.TLabel',
                   font=FONTS['title'],
                   foreground=COLORS['primary'],
                   background=COLORS['bg_primary'])

    style.configure('Heading.TLabel',
                   font=FONTS['heading'],
                   foreground=COLORS['primary'],
                   background=COLORS['bg_primary'])

    style.configure('Secondary.TLabel',
                   font=FONTS['body'],
                   foreground=COLORS['text_secondary'],
                   background=COLORS['bg_primary'])

    # Estilo para Entry
    style.configure('TEntry',
                   fieldbackground=COLORS['bg_secondary'],
                   foreground=COLORS['text_primary'],
                   borderwidth=1,
                   relief='solid')

    # Estilo para Button
    style.configure('TButton',
                   font=FONTS['button'],
                   borderwidth=0,
                   relief='flat',
                   padding=(20, 10))

    style.map('TButton',
             background=[('active', COLORS['accent_light']),
                        ('!active', COLORS['accent'])],
             foreground=[('active', COLORS['text_light']),
                        ('!active', COLORS['text_light'])])

    # Botón primario
    style.configure('Primary.TButton',
                   font=FONTS['button'],
                   background=COLORS['primary'],
                   foreground=COLORS['text_light'])

    style.map('Primary.TButton',
             background=[('active', COLORS['primary_light']),
                        ('!active', COLORS['primary'])])

    # Botón de éxito
    style.configure('Success.TButton',
                   background=COLORS['success'],
                   foreground=COLORS['text_light'])

    style.map('Success.TButton',
             background=[('active', '#2ECC71'),
                        ('!active', COLORS['success'])])

    # Botón de peligro
    style.configure('Danger.TButton',
                   background=COLORS['danger'],
                   foreground=COLORS['text_light'])

    style.map('Danger.TButton',
             background=[('active', '#EC7063'),
                        ('!active', COLORS['danger'])])

    # Estilo para Combobox
    style.configure('TCombobox',
                   fieldbackground=COLORS['bg_secondary'],
                   foreground=COLORS['text_primary'],
                   borderwidth=1)

    # Estilo para Treeview
    style.configure('Treeview',
                   background=COLORS['bg_secondary'],
                   foreground=COLORS['text_primary'],
                   fieldbackground=COLORS['bg_secondary'],
                   borderwidth=1,
                   font=FONTS['body'])

    style.configure('Treeview.Heading',
                   background=COLORS['primary'],
                   foreground=COLORS['text_light'],
                   font=FONTS['subheading'],
                   borderwidth=1)

    style.map('Treeview.Heading',
             background=[('active', COLORS['primary_light']),
                        ('!active', COLORS['primary'])])

    style.map('Treeview',
             background=[('selected', COLORS['accent']),
                        ('!selected', COLORS['bg_secondary'])],
             foreground=[('selected', COLORS['text_light']),
                        ('!selected', COLORS['text_primary'])])

    # Estilo para Notebook (pestañas)
    style.configure('TNotebook',
                   background=COLORS['bg_primary'],
                   borderwidth=0)

    style.configure('TNotebook.Tab',
                   background=COLORS['bg_primary'],
                   foreground=COLORS['text_primary'],
                   padding=(20, 10),
                   font=FONTS['body'])

    style.map('TNotebook.Tab',
             background=[('selected', COLORS['accent']),
                        ('!selected', COLORS['bg_primary'])],
             foreground=[('selected', COLORS['text_light']),
                        ('!selected', COLORS['text_primary'])])

    # Estilo para Separator
    style.configure('TSeparator',
                   background=COLORS['border'])

    return style

def apply_hover_effect(widget, enter_color, leave_color):
    """
    Aplica efecto hover a un widget

    Args:
        widget: Widget al que aplicar el efecto
        enter_color: Color al pasar el mouse
        leave_color: Color al salir el mouse
    """
    def on_enter(e):
        widget['background'] = enter_color

    def on_leave(e):
        widget['background'] = leave_color

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

def create_card_frame(parent, **kwargs):
    """
    Crea un frame con estilo de tarjeta

    Args:
        parent: Widget padre
        **kwargs: Argumentos adicionales para el Frame

    Returns:
        Frame con estilo de tarjeta
    """
    card = ttk.Frame(parent, style='Card.TFrame', **kwargs)
    return card

def create_gradient_label(parent, text, from_color, to_color, height=100, **kwargs):
    """
    Crea una etiqueta con efecto de gradiente (simulado con colores)

    Args:
        parent: Widget padre
        text: Texto a mostrar
        from_color: Color inicial
        to_color: Color final
        height: Altura del gradiente
        **kwargs: Argumentos adicionales

    Returns:
        Frame con la etiqueta
    """
    import tkinter as tk

    frame = tk.Frame(parent, bg=from_color, height=height, **kwargs)
    label = tk.Label(frame, text=text, bg=from_color, fg=COLORS['text_light'],
                    font=FONTS['title'], pady=20)
    label.pack(fill=tk.BOTH, expand=True)

    return frame
