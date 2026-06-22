"""
models.py - Definicion de clases del modelo
POO: encapsulamiento, abstraccion, herencia y polimorfismo
"""
from datetime import datetime
from typing import List, Optional

class Cliente:
    """
    Clase Cliente - Representa a un cliente de la veterinaria.
    Encapsulamiento: atributos privados con getters/setters.
    """
    
    def __init__(self, nombre: str, apellido: str, dni: str = "", 
                 telefono: str = "", email: str = "", direccion: str = ""):
        self._id = None
        self._nombre = nombre
        self._apellido = apellido
        self._dni = dni
        self._telefono = telefono
        self._email = email
        self._direccion = direccion
        self._activo = True
        self._mascotas: List['Mascota'] = []
        self._created_at = datetime.now()
    
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, value: int):
        self._id = value
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value.strip()
    
    @property
    def apellido(self) -> str:
        return self._apellido
    
    @apellido.setter
    def apellido(self, value: str):
        self._apellido = value.strip()
    
    @property
    def dni(self) -> str:
        return self._dni or ""
    
    @dni.setter
    def dni(self, value: str):
        self._dni = value.strip() if value else ""
    
    @property
    def telefono(self) -> str:
        return self._telefono or ""
    
    @telefono.setter
    def telefono(self, value: str):
        self._telefono = value.strip() if value else ""
    
    @property
    def email(self) -> str:
        return self._email or ""
    
    @email.setter
    def email(self, value: str):
        self._email = value.strip() if value else ""
    
    @property
    def direccion(self) -> str:
        return self._direccion or ""
    
    @direccion.setter
    def direccion(self, value: str):
        self._direccion = value.strip() if value else ""
    
    @property
    def mascotas(self) -> List['Mascota']:
        return self._mascotas.copy()
    
    @property
    def cant_mascotas(self) -> int:
        return len(self._mascotas)
    
    @property
    def nombre_completo(self) -> str:
        return f"{self._apellido}, {self._nombre}"
    
    def agregar_mascota(self, mascota: 'Mascota'):
        """Agrega una mascota a la lista (composicion)."""
        if mascota not in self._mascotas:
            self._mascotas.append(mascota)
            mascota.cliente = self
    
    def eliminar_mascota(self, mascota: 'Mascota'):
        """Elimina una mascota de la lista."""
        if mascota in self._mascotas:
            self._mascotas.remove(mascota)
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para la BD."""
        return {
            "nombre": self._nombre,
            "apellido": self._apellido,
            "dni": self._dni,
            "telefono": self._telefono,
            "email": self._email,
            "direccion": self._direccion,
        }
    
    def __str__(self) -> str:
        mascotas_str = f"({self.cant_mascotas} mascota{'s' if self.cant_mascotas != 1 else ''})"
        return f"ID: {self._id} - {self.nombre_completo} {mascotas_str}"


class Animal:
    """
    Clase base para demostrar herencia y polimorfismo.
    """
    def __init__(self, nombre: str, especie: str = "Animal"):
        self._nombre = nombre
        self._especie = especie
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def especie(self) -> str:
        return self._especie
    
    def obtener_descripcion(self) -> str:
        """Metodo polimorfico - sera sobrescrito por las subclases."""
        return f"Animal: {self._nombre}"
    
    def obtener_sonido(self) -> str:
        """Metodo polimorfico - sera sobrescrito por las subclases."""
        return "Sonido generico"
    
    def __str__(self) -> str:
        return f"{self._especie}: {self._nombre}"


class Perro(Animal):
    """Subclase de Animal - demuestra herencia y polimorfismo."""
    def __init__(self, nombre: str, raza: str = ""):
        super().__init__(nombre, "Perro")
        self._raza = raza
    
    @property
    def raza(self) -> str:
        return self._raza
    
    def obtener_descripcion(self) -> str:
        """Sobrescritura del metodo polimorfico."""
        raza_str = f" de raza {self._raza}" if self._raza else ""
        return f"Perro{raza_str} llamado {self._nombre}"
    
    def obtener_sonido(self) -> str:
        """Sobrescritura del metodo polimorfico."""
        return "Guau guau"
    
    def __str__(self) -> str:
        return f"Perro: {self._nombre} {f'({self._raza})' if self._raza else ''}"


class Gato(Animal):
    """Subclase de Animal - demuestra herencia y polimorfismo."""
    def __init__(self, nombre: str, color: str = ""):
        super().__init__(nombre, "Gato")
        self._color = color
    
    @property
    def color(self) -> str:
        return self._color
    
    def obtener_descripcion(self) -> str:
        """Sobrescritura del metodo polimorfico."""
        color_str = f" de color {self._color}" if self._color else ""
        return f"Gato{color_str} llamado {self._nombre}"
    
    def obtener_sonido(self) -> str:
        """Sobrescritura del metodo polimorfico."""
        return "Miau"
    
    def __str__(self) -> str:
        return f"Gato: {self._nombre} {f'({self._color})' if self._color else ''}"


class Mascota:
    """
    Clase Mascota - Representa a una mascota de un cliente.
    Utiliza polimorfismo internamente a traves del metodo crear_animal().
    """
    
    ESPECIES_VALIDAS = ["Perro", "Gato", "Ave", "Conejo", "Reptil", "Otro"]
    SEXOS_VALIDOS = ["M", "F", "desconocido"]
    
    def __init__(self, nombre: str, especie: str, cliente: 'Cliente' = None,
                 raza: str = "", fecha_nac: str = "", sexo: str = "desconocido",
                 peso_kg: float = None, color: str = "", castrado: bool = False):
        self._id = None
        self._nombre = nombre
        self._especie = especie
        self._raza = raza
        self._fecha_nac = fecha_nac
        self._sexo = sexo
        self._peso_kg = peso_kg
        self._color = color
        self._castrado = castrado
        self._activo = True
        self._cliente = cliente
        
        if cliente:
            cliente.agregar_mascota(self)
    
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, value: int):
        self._id = value
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value.strip()
    
    @property
    def especie(self) -> str:
        return self._especie
    
    @especie.setter
    def especie(self, value: str):
        if value in self.ESPECIES_VALIDAS:
            self._especie = value
        else:
            raise ValueError(f"Especie invalida. Debe ser: {', '.join(self.ESPECIES_VALIDAS)}")
    
    @property
    def cliente(self) -> Optional['Cliente']:
        return self._cliente
    
    @cliente.setter
    def cliente(self, value: 'Cliente'):
        self._cliente = value
    
    @property
    def nombre_cliente(self) -> str:
        return self._cliente.nombre_completo if self._cliente else "Sin asignar"
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para la BD."""
        return {
            "nombre": self._nombre,
            "especie": self._especie,
            "raza": self._raza,
            "fecha_nac": self._fecha_nac,
            "sexo": self._sexo,
            "peso_kg": self._peso_kg,
            "color": self._color,
            "castrado": self._castrado,
        }
    
    def crear_animal(self) -> Animal:
        """
        Metodo factory que demuestra polimorfismo.
        Crea un objeto Animal de la subclase correspondiente segun la especie.
        """
        if self._especie == "Perro":
            return Perro(self._nombre, self._raza)
        elif self._especie == "Gato":
            return Gato(self._nombre, self._color)
        else:
            return Animal(self._nombre, self._especie)
    
    def obtener_descripcion_completa(self) -> str:
        """
        Utiliza polimorfismo para obtener la descripcion del animal.
        El metodo crear_animal() devuelve el tipo adecuado.
        """
        animal = self.crear_animal()
        return animal.obtener_descripcion()
    
    def obtener_sonido(self) -> str:
        """Utiliza polimorfismo para obtener el sonido del animal."""
        animal = self.crear_animal()
        return animal.obtener_sonido()
    
    def __str__(self) -> str:
        sexo_str = {"M": "Macho", "F": "Hembra", "desconocido": ""}.get(self._sexo, "")
        return (f"ID: {self._id} - {self._nombre} ({self._especie})"
                f"{f' - {self._raza}' if self._raza else ''}"
                f"{f' - {sexo_str}' if sexo_str else ''}")