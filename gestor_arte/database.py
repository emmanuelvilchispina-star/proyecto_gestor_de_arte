"""
Módulo de conexión a MongoDB para el Gestor de Arte y Artistas
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import sys

class Database:
    def __init__(self, host='localhost', port=27017, db_name='gestor_arte'):
        """
        Inicializa la conexión a MongoDB

        Args:
            host: Host de MongoDB (default: localhost)
            port: Puerto de MongoDB (default: 27017)
            db_name: Nombre de la base de datos (default: gestor_arte)
        """
        try:
            self.client = MongoClient(host, port, serverSelectionTimeoutMS=5000)
            # Verificar conexión
            self.client.admin.command('ping')
            self.db = self.client[db_name]
            print("Conexión exitosa a MongoDB")
        except ConnectionFailure as e:
            print(f"Error al conectar a MongoDB: {e}")
            print("Asegúrate de que MongoDB esté ejecutándose")
            sys.exit(1)

    def get_collection(self, collection_name):
        """
        Obtiene una colección de la base de datos

        Args:
            collection_name: Nombre de la colección

        Returns:
            Colección de MongoDB
        """
        return self.db[collection_name]

    def close(self):
        """Cierra la conexión a MongoDB"""
        if self.client:
            self.client.close()
            print("Conexión a MongoDB cerrada")

# Instancia global de la base de datos
db_instance = None

def get_db():
    """
    Obtiene la instancia global de la base de datos

    Returns:
        Instancia de Database
    """
    global db_instance
    if db_instance is None:
        db_instance = Database()
    return db_instance

