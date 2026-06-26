# Trabajo Practico Integrador (TPI) - Programacion Avanzada 2026


**Alta de Clientes y Mascotas en un Sistema de Gestion Veterinaria**
Comision:2

Autores:
   - Andrade, David
   - Cruz, Solange
   - Gomez Bonacorsi, Emiliano
   - Prieto, Sebastian

## Descripcion

VetApp es un sistema de gestion para clinicas veterinarias desarrollado en Python que permite administrar clientes y sus mascotas. Demuestra la aplicacion de conceptos fundamentales de Programacion Orientada a Objetos, Patrones de Diseño y Modelado UML.

## Estructura del Proyecto

alta_de_clientes_y_mascotas/
├── main.py # Punto de entrada
├── menu.py # Menu interactivo
├── models.py # Modelos de datos (POO)
├── database.py # Capa de acceso a datos
├── gestor.py # Gestor (Singleton)
├── vetapp.db # Base de datos SQLite
├── README.md # Documentacion
└── diagrama_uml.png # Diagrama de clases UML

text

## Requisitos

- Python 3.8 o superior
- SQLite3 (incluido en Python)

## Instalacion y Ejecucion

```bash
# 1. Clonar el repositorio
git clone https://github.com/Solange-Cruz/alta_de_clientes_y_mascotas

# 2. Navegar al directorio
cd alta_de_clientes_y_mascotas

# 3. Ejecutar la aplicacion
python main.py

Conceptos POO Aplicados

1. Encapsulamiento
Los atributos de las clases son privados (convencion _) y se accede mediante getters y setters.

python
class Cliente:
    def __init__(self, nombre, apellido):
        self._nombre = nombre      # Atributo privado
        self._apellido = apellido
    
    @property
    def nombre(self):
        return self._nombre        # Getter
    
    @nombre.setter
    def nombre(self, value):
        self._nombre = value.strip()  # Setter con validacion

2. Abstraccion
Las clases modelan entidades del mundo real: Cliente, Animal, Mascota.

3. Herencia
La clase Animal es la clase base, y Perro y Gato son subclases que heredan de ella.

python
class Animal:
    def obtener_descripcion(self):
        return "Animal generico"

class Perro(Animal):
    def obtener_descripcion(self):
        return "Perro especifico"

class Gato(Animal):
    def obtener_descripcion(self):
        return "Gato especifico"

4. Polimorfismo
El metodo obtener_descripcion() se comporta de manera diferente segun la subclase. Esto se demuestra en el metodo Mascota.crear_animal() y en las operaciones de listado.

python
def crear_animal(self) -> Animal:
    if self._especie == "Perro":
        return Perro(self._nombre, self._raza)
    elif self._especie == "Gato":
        return Gato(self._nombre, self._color)
    else:
        return Animal(self._nombre, self._especie)

5. Composicion
La clase Cliente contiene una lista de Mascotas (relacion de composicion).

Patron de Diseño Implementado
Singleton - GestorVeterinaria
Garantiza una unica instancia del gestor de la aplicacion.

python
class GestorVeterinaria:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

Clases Principales
-------------------------------------------------------------------------------------------------
Clase	            | Descripcion	                                  | Conceptos POO
-------------------------------------------------------------------------------------------------
Cliente	         | Representa un cliente	                         | Encapsulamiento, Abstraccion
Mascota	         | Representa una mascota	                      | Encapsulamiento, Composicion
GestorVeterinaria | Gestiona operaciones del sistema	             | Singleton.
Animal	         | Clase base para demostrar herencia	          | Herencia, Polimorfismo
Perro/Gato	      | Subclases de Animal	                         | Herencia, Polimorfismo
--------------------------------------------------------------------------------------------------

Base de Datos
   Tabla cliente
      id (INTEGER, PK)
      nombre (TEXT)
      apellido (TEXT)
      dni (TEXT, UNIQUE)
      telefono (TEXT)
      email (TEXT)
      direccion (TEXT)
      activo (INTEGER)
      created_at (TEXT)

   Tabla mascota
      id (INTEGER, PK)
      cliente_id (INTEGER, FK)
      nombre (TEXT)
      especie (TEXT)
      raza (TEXT)
      fecha_nac (TEXT)
      sexo (TEXT)
      peso_kg (REAL)
      color (TEXT)
      castrado (INTEGER)
      activo (INTEGER)

Funcionalidades
   Gestion de clientes (CRUD)
   Gestion de mascotas (CRUD)
   Busqueda de clientes y mascotas
   Visualizacion de relaciones cliente-mascota


Diagrama UML


Licencia
Proyecto educativo - Programacion Avanzada 2026
