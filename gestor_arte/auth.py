"""
Módulo de autenticación para el Gestor de Arte y Artistas
"""
import hashlib
from database import get_db

class AuthManager:
    def __init__(self):
        """Inicializa el gestor de autenticación"""
        self.db = get_db()
        self.usuarios_collection = self.db.get_collection('usuarios')

    def hash_password(self, password):
        """
        Hashea una contraseña usando SHA-256

        Args:
            password: Contraseña en texto plano

        Returns:
            Contraseña hasheada
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, username, password):
        """
        Autentica un usuario

        Args:
            username: Nombre de usuario
            password: Contraseña

        Returns:
            Diccionario con información del usuario si es exitoso, None si falla
        """
        hashed_password = self.hash_password(password)
        usuario = self.usuarios_collection.find_one({
            'username': username,
            'password': hashed_password
        })

        if usuario:
            return {
                'username': usuario['username'],
                'rol': usuario['rol']
            }
        return None

    def get_user_permissions(self, rol):
        """
        Obtiene los módulos permitidos para un rol

        Args:
            rol: Rol del usuario (Curador, Administrador, Usuario)

        Returns:
            Lista de módulos permitidos
        """
        permissions = {
            'Curador': ['artistas', 'obras'],
            'Administrador': ['exposiciones', 'subastas', 'usuarios'],
            'Usuario': ['busqueda']
        }
        return permissions.get(rol, [])

    def create_user(self, username, password, rol):
        """
        Crea un nuevo usuario (método administrativo)

        Args:
            username: Nombre de usuario
            password: Contraseña
            rol: Rol del usuario

        Returns:
            True si se creó exitosamente, False si ya existe
        """
        if self.usuarios_collection.find_one({'username': username}):
            return False

        hashed_password = self.hash_password(password)
        self.usuarios_collection.insert_one({
            'username': username,
            'password': hashed_password,
            'rol': rol
        })
        return True
