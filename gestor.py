"""
gestor.py - Gestor de la veterinaria (Patron Singleton)
"""
from typing import List, Optional, Dict, Any
from models import Cliente, Mascota
from database import (
    get_clientes, get_cliente, buscar_cliente,
    crear_cliente, actualizar_cliente, eliminar_cliente,
    get_mascotas_cliente, get_mascota, buscar_mascota,
    crear_mascota, actualizar_mascota, eliminar_mascota
)

class GestorVeterinaria:
    """
    Clase Singleton que gestiona todas las operaciones de la veterinaria.
    Patron de Diseño: Singleton - garantiza una unica instancia.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GestorVeterinaria, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._clientes_cache: Dict[int, Cliente] = {}
    
    def listar_clientes(self) -> List[Cliente]:
        """Lista todos los clientes como objetos Cliente."""
        clientes_data = get_clientes()
        clientes = []
        for c_data in clientes_data:
            cliente = Cliente(
                c_data["nombre"], c_data["apellido"],
                c_data.get("dni", ""), c_data.get("telefono", ""),
                c_data.get("email", ""), c_data.get("direccion", "")
            )
            cliente.id = c_data["id"]
            clientes.append(cliente)
            self._clientes_cache[cliente.id] = cliente
        return clientes
    
    def obtener_cliente(self, cliente_id: int) -> Optional[Cliente]:
        """Obtiene un cliente por ID."""
        if cliente_id in self._clientes_cache:
            return self._clientes_cache[cliente_id]
        
        c_data = get_cliente(cliente_id)
        if not c_data:
            return None
        
        cliente = Cliente(
            c_data["nombre"], c_data["apellido"],
            c_data.get("dni", ""), c_data.get("telefono", ""),
            c_data.get("email", ""), c_data.get("direccion", "")
        )
        cliente.id = c_data["id"]
        self._clientes_cache[cliente.id] = cliente
        return cliente
    
    def buscar_cliente(self, termino: str) -> List[Cliente]:
        """Busca clientes por termino."""
        clientes_data = buscar_cliente(termino)
        clientes = []
        for c_data in clientes_data:
            cliente = Cliente(
                c_data["nombre"], c_data["apellido"],
                c_data.get("dni", ""), c_data.get("telefono", ""),
                c_data.get("email", ""), c_data.get("direccion", "")
            )
            cliente.id = c_data["id"]
            clientes.append(cliente)
        return clientes
    
    def crear_cliente(self, cliente: Cliente) -> int:
        """Crea un nuevo cliente."""
        data = cliente.to_dict()
        cliente_id = crear_cliente(data)
        cliente.id = cliente_id
        self._clientes_cache[cliente_id] = cliente
        return cliente_id
    
    def actualizar_cliente(self, cliente: Cliente) -> bool:
        """Actualiza un cliente existente."""
        if not cliente.id:
            return False
        actualizar_cliente(cliente.id, cliente.to_dict())
        self._clientes_cache[cliente.id] = cliente
        return True
    
    def eliminar_cliente(self, cliente_id: int) -> tuple:
        """Elimina un cliente si no tiene mascotas."""
        mascotas = self.listar_mascotas_cliente(cliente_id)
        if mascotas:
            return False, "No se puede eliminar: el cliente tiene mascotas activas."
        
        if eliminar_cliente(cliente_id):
            self._clientes_cache.pop(cliente_id, None)
            return True, "Cliente eliminado correctamente."
        return False, "Error al eliminar el cliente."
    
    def listar_mascotas_cliente(self, cliente_id: int) -> List[Mascota]:
        """Lista todas las mascotas de un cliente."""
        mascotas_data = get_mascotas_cliente(cliente_id)
        mascotas = []
        for m_data in mascotas_data:
            mascota = Mascota(
                m_data["nombre"], m_data["especie"],
                None, m_data.get("raza", ""),
                m_data.get("fecha_nac", ""), m_data.get("sexo", "desconocido"),
                m_data.get("peso_kg"), m_data.get("color", ""),
                bool(m_data.get("castrado", 0))
            )
            mascota.id = m_data["id"]
            cliente = self.obtener_cliente(cliente_id)
            if cliente:
                mascota.cliente = cliente
            mascotas.append(mascota)
        return mascotas
    
    def obtener_mascota(self, mascota_id: int) -> Optional[Mascota]:
        """Obtiene una mascota por ID."""
        m_data = get_mascota(mascota_id)
        if not m_data:
            return None
        
        mascota = Mascota(
            m_data["nombre"], m_data["especie"],
            None, m_data.get("raza", ""),
            m_data.get("fecha_nac", ""), m_data.get("sexo", "desconocido"),
            m_data.get("peso_kg"), m_data.get("color", ""),
            bool(m_data.get("castrado", 0))
        )
        mascota.id = m_data["id"]
        return mascota
    
    def buscar_mascota(self, termino: str) -> List[Dict[str, Any]]:
        """Busca mascotas por nombre o propietario."""
        return buscar_mascota(termino)
    
    def crear_mascota(self, cliente_id: int, mascota: Mascota) -> int:
        """Crea una nueva mascota para un cliente."""
        data = mascota.to_dict()
        data["cliente_id"] = cliente_id
        mascota_id = crear_mascota(data)
        mascota.id = mascota_id
        
        cliente = self.obtener_cliente(cliente_id)
        if cliente:
            cliente.agregar_mascota(mascota)
            mascota.cliente = cliente
        
        return mascota_id
    
    def actualizar_mascota(self, mascota: Mascota) -> bool:
        """Actualiza una mascota existente."""
        if not mascota.id:
            return False
        actualizar_mascota(mascota.id, mascota.to_dict())
        return True
    
    def eliminar_mascota(self, mascota_id: int) -> bool:
        """Elimina una mascota."""
        return eliminar_mascota(mascota_id)
    
    def obtener_info_completa_mascota(self, mascota_id: int) -> str:
        """
        Demuestra el polimorfismo en accion.
        Obtiene una mascota y utiliza sus metodos polimorficos.
        """
        mascota = self.obtener_mascota(mascota_id)
        if not mascota:
            return "Mascota no encontrada"
        
        descripcion = mascota.obtener_descripcion_completa()
        sonido = mascota.obtener_sonido()
        
        return f"{descripcion} - {sonido}"