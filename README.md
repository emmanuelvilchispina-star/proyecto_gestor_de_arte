# Gestor de Perfiles de Arte y Artistas

Aplicación de gestión de arte desarrollada con Python, Tkinter y MongoDB.

## Descripción

Sistema completo para la gestión de artistas, obras de arte, exposiciones y subastas con control de acceso basado en roles.

## Requisitos Previos

- Python 3.8 o superior
- MongoDB Community Edition 4.4 o superior

## Instalación

### 1. Instalar MongoDB

**Windows:**
1. Descargar MongoDB Community Edition desde https://www.mongodb.com/try/download/community
2. Ejecutar el instalador
3. Durante la instalación, seleccionar "Install MongoDB as a Service"
4. Completar la instalación

**Linux:**
```bash
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

### 2. Verificar que MongoDB está ejecutándose

**Windows:**
- Abrir "Servicios" y buscar "MongoDB Server"
- Verificar que el estado sea "En ejecución"

**Linux/macOS:**
```bash
sudo systemctl status mongod  # Linux
brew services list             # macOS
```

### 3. Instalar dependencias de Python

```bash
cd gestor_arte
pip install -r requirements.txt
```

### 4. Inicializar la base de datos

```bash
python init_db.py
```

Este script creará:
- 3 usuarios de prueba
- 4 artistas de ejemplo
- 8 obras de arte
- 3 exposiciones
- 3 valoraciones con historial de ofertas

## Ejecución

```bash
python main.py
```

## Usuarios de Prueba

| Usuario  | Contraseña   | Rol            | Módulos Accesibles                      |
|----------|--------------|----------------|-----------------------------------------|
| curador  | curador123   | Curador        | Artistas, Obras                         |
| admin    | admin123     | Administrador  | Exposiciones, Subastas, Usuarios        |
| usuario  | usuario123   | Usuario        | Búsqueda                                |

## Módulos del Sistema

### 1. Registro de Artistas (Curador)
- CRUD completo de artistas
- Gestión de biografías y enlaces
- Registro de fecha de nacimiento y país

### 2. Catálogo de Obras (Curador)
- CRUD de obras de arte
- Metadatos específicos por técnica:
  - **Pintura:** Pigmento, dimensiones, soporte
  - **Escultura:** Material, dimensiones, peso
  - **Fotografía:** Técnica fotográfica, formato, edición
- Vinculación con artistas

### 3. Módulo de Exposiciones (Administrador)
- Creación de exposiciones
- Agrupación de obras por tema o artista
- Gestión de fechas y descripciones

### 4. Valoraciones y Subastas (Administrador)
- Registro de valoraciones de obras
- Historial de ofertas de subasta
- Seguimiento de perito/tasador
- Múltiples monedas (USD, EUR, MXN, ARS, COP)

### 5. Búsqueda por Atributo (Usuario)
- Búsqueda por texto en título y descripción
- Filtros por artista, técnica y año
- Búsqueda avanzada en metadatos
- Vista detallada de obras con información completa

### 6. Gestión de Usuarios (Administrador)
- CRUD completo de usuarios del sistema
- Asignación de roles (Curador, Administrador, Usuario)
- Gestión de contraseñas seguras (SHA-256)
- Control de permisos por rol
- Interfaz intuitiva para administración de usuarios

## Características del Diseño Visual

La aplicación cuenta con un diseño moderno y profesional:
- **Interfaz mejorada** con colores elegantes y tipografía moderna
- **Tarjetas interactivas** con efectos hover
- **Header personalizado** con información del usuario
- **Paleta de colores consistente** en toda la aplicación
- **Iconos visuales** para mejor identificación de módulos
- **Diseño responsivo** y organizado

## Estructura del Proyecto

```
gestor_arte/
├── main.py                 # Aplicación principal (login y menú mejorado)
├── database.py             # Conexión a MongoDB
├── auth.py                 # Sistema de autenticación
├── styles.py               # Estilos y tema visual de la aplicación
├── init_db.py              # Script de inicialización
├── requirements.txt        # Dependencias
├── README.md              # Documentación
├── modulos/
│   ├── __init__.py
│   ├── artistas.py         # Módulo 1: Registro de Artistas
│   ├── obras.py            # Módulo 2: Catálogo de Obras
│   ├── exposiciones.py     # Módulo 3: Exposiciones
│   ├── subastas.py         # Módulo 4: Valoraciones y Subastas
│   ├── busqueda.py         # Módulo 5: Búsqueda por Atributo
│   └── usuarios.py         # Módulo 6: Gestión de Usuarios
└── wireframes/            # Carpeta para diseños
```

## Colecciones de MongoDB

### usuarios
```javascript
{
  username: String,
  password: String (SHA-256),
  rol: String (Curador|Administrador|Usuario)
}
```

### artistas
```javascript
{
  _id: ObjectId,
  nombre: String,
  pais: String,
  fecha_nacimiento: Date,
  biografia: String,
  enlaces: [String]
}
```

### obras
```javascript
{
  _id: ObjectId,
  titulo: String,
  artista_id: String,
  tecnica: String,
  anio: Number,
  descripcion: String,
  metadatos: {
    // Campos específicos según técnica
  }
}
```

### exposiciones
```javascript
{
  _id: ObjectId,
  nombre: String,
  tema: String,
  fecha_inicio: Date,
  fecha_fin: Date,
  descripcion: String,
  obras: [ObjectId]
}
```

### valoraciones
```javascript
{
  _id: ObjectId,
  obra_id: String,
  valoracion_actual: Number,
  moneda: String,
  fecha_valoracion: Date,
  perito: String,
  historial_ofertas: [
    {
      fecha: Date,
      ofertante: String,
      monto: Number
    }
  ]
}
```

## Solución de Problemas

### Error: "No se puede conectar a MongoDB"
- Verificar que MongoDB esté ejecutándose
- Comprobar que el puerto 27017 esté disponible
- En Windows, revisar el servicio "MongoDB Server"

### Error: "ModuleNotFoundError: No module named 'pymongo'"
```bash
pip install pymongo
```

### Error al inicializar la base de datos
- Asegurarse de que MongoDB esté ejecutándose
- Verificar permisos de escritura en la base de datos

## Características Técnicas

- **Interfaz:** Tkinter (GUI nativa de Python)
- **Base de Datos:** MongoDB (NoSQL)
- **Autenticación:** SHA-256 para contraseñas
- **Arquitectura:** Modular con separación de responsabilidades
- **Control de Acceso:** Basado en roles


## Autores

Proyecto desarrollado por:
- Emmanuel Alejandro Vilchis Piña
- Adrian Laredo Reyes
- Pablo Reyes Alvarez
- Diego Edu Diaz Leon


## Licencia

Este proyecto es de uso educativo.
