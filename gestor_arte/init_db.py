"""
Script de inicialización de la base de datos
Crea usuarios de prueba y datos de ejemplo
"""
from database import get_db
from auth import AuthManager
from datetime import datetime
from bson.objectid import ObjectId  # <--- IMPORTANTE: Agregado para manejar IDs

def init_database():
    """Inicializa la base de datos con datos de prueba"""
    print("Iniciando configuración de la base de datos...")

    db = get_db()
    auth = AuthManager()

    # Limpiar colecciones existentes
    print("\nLimpiando colecciones existentes...")
    db.get_collection('usuarios').delete_many({})
    db.get_collection('artistas').delete_many({})
    db.get_collection('obras').delete_many({})
    db.get_collection('exposiciones').delete_many({})
    db.get_collection('valoraciones').delete_many({})

    # Crear usuarios de prueba
    print("\nCreando usuarios de prueba...")

    usuarios = [
        {'username': 'curador', 'password': 'curador123', 'rol': 'Curador'},
        {'username': 'admin', 'password': 'admin123', 'rol': 'Administrador'},
        {'username': 'usuario', 'password': 'usuario123', 'rol': 'Usuario'}
    ]

    for user in usuarios:
        auth.create_user(user['username'], user['password'], user['rol'])
        print(f"  ✓ Usuario creado: {user['username']} ({user['rol']})")

    # Crear artistas de ejemplo
    print("\nCreando artistas de ejemplo...")

    artistas = [
        {
            'nombre': 'Frida Kahlo',
            'pais': 'México',
            'fecha_nacimiento': datetime(1907, 7, 6),
            'biografia': 'Pintora mexicana conocida por sus autorretratos y obras inspiradas en la naturaleza y artefactos de México.',
            'enlaces': ['https://www.fridakahlo.org/', 'https://es.wikipedia.org/wiki/Frida_Kahlo']
        },
        {
            'nombre': 'Diego Rivera',
            'pais': 'México',
            'fecha_nacimiento': datetime(1886, 12, 8),
            'biografia': 'Destacado muralista mexicano, esposo de Frida Kahlo. Sus murales establecieron el Movimiento Mural Mexicano.',
            'enlaces': ['https://www.diegorivera.org/', 'https://es.wikipedia.org/wiki/Diego_Rivera']
        },
        {
            'nombre': 'Fernando Botero',
            'pais': 'Colombia',
            'fecha_nacimiento': datetime(1932, 4, 19),
            'biografia': 'Pintor y escultor colombiano, conocido por su estilo figurativo con volúmenes exagerados.',
            'enlaces': ['https://www.botero.com/']
        },
        {
            'nombre': 'Remedios Varo',
            'pais': 'España',
            'fecha_nacimiento': datetime(1908, 12, 16),
            'biografia': 'Pintora surrealista española exiliada en México, conocida por sus obras místicas y oníricas.',
            'enlaces': ['https://es.wikipedia.org/wiki/Remedios_Varo']
        }
    ]

    artistas_collection = db.get_collection('artistas')
    artistas_ids = {}

    for artista in artistas:
        result = artistas_collection.insert_one(artista)
        artistas_ids[artista['nombre']] = str(result.inserted_id)
        print(f"  ✓ Artista creado: {artista['nombre']}")

    # Crear obras de ejemplo
    print("\nCreando obras de ejemplo...")

    obras = [
        {
            'titulo': 'Las Dos Fridas',
            'artista_id': artistas_ids['Frida Kahlo'],
            'tecnica': 'Pintura',
            'anio': 1939,
            'descripcion': 'Doble autorretrato que representa dos personalidades de Frida.',
            'metadatos': {
                'pigmento': 'Óleo',
                'dimensiones': '173.5 x 173 cm',
                'soporte': 'Lienzo'
            }
        },
        {
            'titulo': 'La Columna Rota',
            'artista_id': artistas_ids['Frida Kahlo'],
            'tecnica': 'Pintura',
            'anio': 1944,
            'descripcion': 'Autorretrato que muestra el dolor físico y emocional de Frida.',
            'metadatos': {
                'pigmento': 'Óleo',
                'dimensiones': '40 x 30.7 cm',
                'soporte': 'Lienzo sobre masonite'
            }
        },
        {
            'titulo': 'Sueño de una tarde dominical en la Alameda Central',
            'artista_id': artistas_ids['Diego Rivera'],
            'tecnica': 'Pintura',
            'anio': 1947,
            'descripcion': 'Mural que representa 400 años de historia mexicana.',
            'metadatos': {
                'pigmento': 'Pintura mural',
                'dimensiones': '4.8 x 15 m',
                'soporte': 'Muro'
            }
        },
        {
            'titulo': 'El Hombre Controlador del Universo',
            'artista_id': artistas_ids['Diego Rivera'],
            'tecnica': 'Pintura',
            'anio': 1934,
            'descripcion': 'Mural recreado en el Palacio de Bellas Artes de México.',
            'metadatos': {
                'pigmento': 'Fresco',
                'dimensiones': '4.85 x 11.45 m',
                'soporte': 'Muro'
            }
        },
        {
            'titulo': 'La Familia Presidencial',
            'artista_id': artistas_ids['Fernando Botero'],
            'tecnica': 'Pintura',
            'anio': 1967,
            'descripcion': 'Sátira política con las figuras volumétricas características de Botero.',
            'metadatos': {
                'pigmento': 'Óleo',
                'dimensiones': '203.5 x 196.2 cm',
                'soporte': 'Lienzo'
            }
        },
        {
            'titulo': 'Mujer con Espejo',
            'artista_id': artistas_ids['Fernando Botero'],
            'tecnica': 'Escultura',
            'anio': 2004,
            'descripcion': 'Escultura monumental en bronce con el estilo volumétrico de Botero.',
            'metadatos': {
                'material': 'Bronce',
                'dimensiones': '195 x 89 x 68 cm',
                'peso': '350 kg'
            }
        },
        {
            'titulo': 'La Creación de las Aves',
            'artista_id': artistas_ids['Remedios Varo'],
            'tecnica': 'Pintura',
            'anio': 1957,
            'descripcion': 'Obra surrealista que muestra una figura creando aves con un instrumento musical.',
            'metadatos': {
                'pigmento': 'Óleo',
                'dimensiones': '54 x 64 cm',
                'soporte': 'Masonite'
            }
        },
        {
            'titulo': 'Bordando el Manto Terrestre',
            'artista_id': artistas_ids['Remedios Varo'],
            'tecnica': 'Pintura',
            'anio': 1961,
            'descripcion': 'Niñas en una torre bordando un tapiz que se convierte en el mundo exterior.',
            'metadatos': {
                'pigmento': 'Óleo',
                'dimensiones': '100 x 123 cm',
                'soporte': 'Masonite'
            }
        }
    ]

    obras_collection = db.get_collection('obras')
    obras_ids = []

    for obra in obras:
        result = obras_collection.insert_one(obra)
        obras_ids.append(result.inserted_id)
        print(f"  ✓ Obra creada: {obra['titulo']}")

    # Crear exposiciones de ejemplo
    print("\nCreando exposiciones de ejemplo...")

    exposiciones = [
        {
            'nombre': 'Arte Mexicano del Siglo XX',
            'tema': 'Arte Mexicano',
            'fecha_inicio': datetime(2024, 1, 15),
            'fecha_fin': datetime(2024, 3, 15),
            'descripcion': 'Exhibición de las principales obras del arte mexicano del siglo XX.',
            'obras': [obras_ids[0], obras_ids[1], obras_ids[2], obras_ids[3]]
        },
        {
            'nombre': 'Surrealismo Latinoamericano',
            'tema': 'Surrealismo',
            'fecha_inicio': datetime(2024, 4, 1),
            'fecha_fin': datetime(2024, 6, 30),
            'descripcion': 'Exploración del movimiento surrealista en América Latina.',
            'obras': [obras_ids[0], obras_ids[6], obras_ids[7]]
        },
        {
            'nombre': 'Botero: Volumen y Forma',
            'tema': 'Escultura Contemporánea',
            'fecha_inicio': datetime(2024, 7, 10),
            'fecha_fin': datetime(2024, 9, 10),
            'descripcion': 'Retrospectiva de la obra escultórica de Fernando Botero.',
            'obras': [obras_ids[4], obras_ids[5]]
        }
    ]

    exposiciones_collection = db.get_collection('exposiciones')

    for expo in exposiciones:
        exposiciones_collection.insert_one(expo)
        print(f"  ✓ Exposición creada: {expo['nombre']}")

    # Crear valoraciones de ejemplo
    print("\nCreando valoraciones de ejemplo...")

    valoraciones = [
        {
            'obra_id': str(obras_ids[0]),
            'valoracion_actual': 15000000,
            'moneda': 'USD',
            'fecha_valoracion': datetime(2023, 5, 10),
            'perito': 'Casa de Subastas Sotheby\'s',
            'historial_ofertas': [
                {'fecha': datetime(2023, 6, 1), 'ofertante': 'Museo Nacional de Arte', 'monto': 14500000},
                {'fecha': datetime(2023, 6, 5), 'ofertante': 'Colección Privada Slim', 'monto': 15000000}
            ]
        },
        {
            'obra_id': str(obras_ids[2]),
            'valoracion_actual': 8500000,
            'moneda': 'USD',
            'fecha_valoracion': datetime(2023, 8, 15),
            'perito': 'Christie\'s',
            'historial_ofertas': [
                {'fecha': datetime(2023, 9, 10), 'ofertante': 'Fundación Diego Rivera', 'monto': 8000000},
                {'fecha': datetime(2023, 9, 12), 'ofertante': 'Museo de Arte Moderno', 'monto': 8500000}
            ]
        },
        {
            'obra_id': str(obras_ids[5]),
            'valoracion_actual': 2500000,
            'moneda': 'USD',
            'fecha_valoracion': datetime(2024, 1, 20),
            'perito': 'Galería Botero',
            'historial_ofertas': [
                {'fecha': datetime(2024, 2, 1), 'ofertante': 'Coleccionista Privado', 'monto': 2300000},
                {'fecha': datetime(2024, 2, 5), 'ofertante': 'Museo de Arte Latinoamericano', 'monto': 2500000}
            ]
        }
    ]

    valoraciones_collection = db.get_collection('valoraciones')

    for val in valoraciones:
        valoraciones_collection.insert_one(val)
        # --- AQUÍ ESTÁ EL CAMBIO PRINCIPAL ---
        # Usamos ObjectId para convertir el texto a un ID válido de Mongo
        obra_id_objeto = ObjectId(val['obra_id'])
        obra = obras_collection.find_one({'_id': obra_id_objeto})
        
        titulo = obra['titulo'] if obra else "Obra desconocida"
        print(f"  ✓ Valoración creada para: {titulo}")

    print("\n" + "="*60)
    print("BASE DE DATOS INICIALIZADA CORRECTAMENTE")
    print("="*60)
    print("\nUSUARIOS DE PRUEBA:")
    print("  Usuario: curador    | Contraseña: curador123  | Rol: Curador")
    print("  Usuario: admin      | Contraseña: admin123    | Rol: Administrador")
    print("  Usuario: usuario    | Contraseña: usuario123  | Rol: Usuario")
    print("\nDATOS CREADOS:")
    print(f"  • {len(artistas)} artistas")
    print(f"  • {len(obras)} obras")
    print(f"  • {len(exposiciones)} exposiciones")
    print(f"  • {len(valoraciones)} valoraciones")
    print("\n¡Ahora puedes ejecutar main.py para iniciar la aplicación!")
    print("="*60)

