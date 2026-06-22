"""
menu.py - Menu interactivo por consola
"""
import os
from typing import Optional
from models import Cliente, Mascota
from gestor import GestorVeterinaria

class MenuVetApp:
    """Menu principal de la aplicacion."""
    
    def __init__(self):
        self.gestor = GestorVeterinaria()
        self._limpiar_pantalla()
    
    def _limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _pausa(self):
        """Pausa la ejecucion hasta que el usuario presione Enter."""
        input("\nPresione Enter para continuar...")
    
    def _mostrar_titulo(self, titulo: str):
        """Muestra un titulo formateado."""
        print("\n" + "=" * 50)
        print(f"  {titulo.upper()}")
        print("=" * 50)
    
    def _mostrar_subtitulo(self, subtitulo: str):
        """Muestra un subtitulo."""
        print(f"\n--- {subtitulo} ---")
    
    def _input_no_vacio(self, mensaje: str) -> str:
        """Solicita un input que no puede estar vacio."""
        while True:
            valor = input(mensaje).strip()
            if valor:
                return valor
            print("Este campo no puede estar vacio.")
    
    def _input_opcional(self, mensaje: str) -> str:
        """Solicita un input opcional."""
        return input(mensaje).strip()
    
    def _seleccionar_cliente(self) -> Optional[Cliente]:
        """Permite seleccionar un cliente de la lista."""
        clientes = self.gestor.listar_clientes()
        if not clientes:
            print("No hay clientes registrados.")
            return None
        
        print("\nClientes disponibles:")
        for i, c in enumerate(clientes, 1):
            print(f"  {i}. {c}")
        
        try:
            opcion = int(input("\nSeleccione numero: "))
            if 1 <= opcion <= len(clientes):
                return clientes[opcion - 1]
        except ValueError:
            pass
        
        print("Seleccion invalida.")
        return None
    
    def _ingresar_cliente(self) -> Cliente:
        """Solicita los datos de un cliente."""
        self._mostrar_subtitulo("DATOS DEL CLIENTE")
        nombre = self._input_no_vacio("Nombre *: ")
        apellido = self._input_no_vacio("Apellido *: ")
        dni = self._input_opcional("DNI (opcional): ")
        telefono = self._input_opcional("Telefono: ")
        email = self._input_opcional("Email: ")
        direccion = self._input_opcional("Direccion: ")
        
        return Cliente(nombre, apellido, dni, telefono, email, direccion)
    
    def _ingresar_mascota(self) -> Mascota:
        """Solicita los datos de una mascota."""
        self._mostrar_subtitulo("DATOS DE LA MASCOTA")
        nombre = self._input_no_vacio("Nombre *: ")
        
        print("\nEspecies disponibles:")
        for i, esp in enumerate(Mascota.ESPECIES_VALIDAS, 1):
            print(f"  {i}. {esp}")
        while True:
            try:
                opc = int(input("Seleccione especie (1-6): "))
                if 1 <= opc <= len(Mascota.ESPECIES_VALIDAS):
                    especie = Mascota.ESPECIES_VALIDAS[opc - 1]
                    break
            except ValueError:
                pass
            print("Seleccion invalida.")
        
        raza = self._input_opcional("Raza: ")
        fecha_nac = self._input_opcional("Fecha de nacimiento (YYYY-MM-DD): ")
        
        print("\nSexo:")
        print("  1. Macho")
        print("  2. Hembra")
        print("  3. Desconocido")
        sexo_opts = {"1": "M", "2": "F", "3": "desconocido"}
        sexo = sexo_opts.get(input("Seleccione (1-3): "), "desconocido")
        
        peso = self._input_opcional("Peso (kg): ")
        color = self._input_opcional("Color: ")
        
        castrado = input("Esta castrado? (s/N): ").lower() == 's'
        
        return Mascota(nombre, especie, None, raza, fecha_nac, sexo, 
                       float(peso) if peso else None, color, castrado)
    
    def mostrar_menu_principal(self):
        """Muestra el menu principal y gestiona la navegacion."""
        while True:
            self._limpiar_pantalla()
            print("\n" + "=" * 50)
            print("   VETAPP - SISTEMA DE GESTION VETERINARIA")
            print("=" * 50)
            print("\n  1. Gestionar Clientes")
            print("  2. Gestionar Mascotas")
            print("  3. Buscar")
            print("  0. Salir")
            print("=" * 50)
            
            opcion = input("\nSeleccione una opcion: ").strip()
            
            if opcion == "1":
                self.menu_clientes()
            elif opcion == "2":
                self.menu_mascotas()
            elif opcion == "3":
                self.menu_buscar()
            elif opcion == "0":
                print("\nGracias por usar VetApp")
                break
            else:
                print("Opcion invalida.")
                self._pausa()
    
    def menu_clientes(self):
        """Menu de gestion de clientes."""
        while True:
            self._limpiar_pantalla()
            self._mostrar_titulo("GESTION DE CLIENTES")
            print("\n  1. Listar clientes")
            print("  2. Crear cliente")
            print("  3. Editar cliente")
            print("  4. Eliminar cliente")
            print("  0. Volver")
            
            opcion = input("\nSeleccione una opcion: ").strip()
            
            if opcion == "1":
                self.listar_clientes()
            elif opcion == "2":
                self.crear_cliente()
            elif opcion == "3":
                self.editar_cliente()
            elif opcion == "4":
                self.eliminar_cliente()
            elif opcion == "0":
                break
            else:
                print("Opcion invalida.")
                self._pausa()
    
    def listar_clientes(self):
        """Lista todos los clientes."""
        self._limpiar_pantalla()
        self._mostrar_titulo("LISTA DE CLIENTES")
        
        clientes = self.gestor.listar_clientes()
        if not clientes:
            print("\nNo hay clientes registrados.")
        else:
            print(f"\nTotal: {len(clientes)} clientes\n")
            print("-" * 70)
            for c in clientes:
                print(c)
        self._pausa()
    
    def crear_cliente(self):
        """Crea un nuevo cliente."""
        self._limpiar_pantalla()
        self._mostrar_titulo("NUEVO CLIENTE")
        
        cliente = self._ingresar_cliente()
        try:
            cliente_id = self.gestor.crear_cliente(cliente)
            print(f"\nCliente creado con ID: {cliente_id}")
        except Exception as e:
            print(f"\nError al crear cliente: {e}")
        self._pausa()
    
    def editar_cliente(self):
        """Edita un cliente existente."""
        self._limpiar_pantalla()
        self._mostrar_titulo("EDITAR CLIENTE")
        
        cliente = self._seleccionar_cliente()
        if not cliente:
            self._pausa()
            return
        
        print(f"\nEditando: {cliente.nombre_completo}")
        print("(Deje vacio para mantener el valor actual)")
        
        nombre = input(f"Nombre [{cliente.nombre}]: ").strip()
        if nombre:
            cliente.nombre = nombre
        
        apellido = input(f"Apellido [{cliente.apellido}]: ").strip()
        if apellido:
            cliente.apellido = apellido
        
        dni = input(f"DNI [{cliente.dni}]: ").strip()
        if dni:
            cliente.dni = dni
        
        telefono = input(f"Telefono [{cliente.telefono}]: ").strip()
        if telefono:
            cliente.telefono = telefono
        
        email = input(f"Email [{cliente.email}]: ").strip()
        if email:
            cliente.email = email
        
        direccion = input(f"Direccion [{cliente.direccion}]: ").strip()
        if direccion:
            cliente.direccion = direccion
        
        try:
            if self.gestor.actualizar_cliente(cliente):
                print("\nCliente actualizado correctamente.")
            else:
                print("\nError al actualizar cliente.")
        except Exception as e:
            print(f"\nError: {e}")
        self._pausa()
    
    def eliminar_cliente(self):
        """Elimina un cliente."""
        self._limpiar_pantalla()
        self._mostrar_titulo("ELIMINAR CLIENTE")
        
        cliente = self._seleccionar_cliente()
        if not cliente:
            self._pausa()
            return
        
        print(f"\nEsta seguro de eliminar a {cliente.nombre_completo}?")
        print("   No se podra eliminar si tiene mascotas activas.")
        confirmar = input("   Confirmar? (s/N): ").lower()
        
        if confirmar == 's':
            exito, mensaje = self.gestor.eliminar_cliente(cliente.id)
            if exito:
                print(f"\n{mensaje}")
            else:
                print(f"\n{mensaje}")
        else:
            print("\nOperacion cancelada.")
        self._pausa()
    
    def menu_mascotas(self):
        """Menu de gestion de mascotas."""
        while True:
            self._limpiar_pantalla()
            self._mostrar_titulo("GESTION DE MASCOTAS")
            print("\n  1. Listar mascotas de un cliente")
            print("  2. Registrar mascota")
            print("  3. Editar mascota")
            print("  4. Eliminar mascota")
            print("  5. Ver informacion completa de una mascota")
            print("  0. Volver")
            
            opcion = input("\nSeleccione una opcion: ").strip()
            
            if opcion == "1":
                self.listar_mascotas()
            elif opcion == "2":
                self.crear_mascota()
            elif opcion == "3":
                self.editar_mascota()
            elif opcion == "4":
                self.eliminar_mascota()
            elif opcion == "5":
                self.ver_info_mascota()
            elif opcion == "0":
                break
            else:
                print("Opcion invalida.")
                self._pausa()
    
    def listar_mascotas(self):
        """Lista las mascotas de un cliente."""
        self._limpiar_pantalla()
        self._mostrar_titulo("MASCOTAS POR CLIENTE")
        
        cliente = self._seleccionar_cliente()
        if not cliente:
            self._pausa()
            return
        
        mascotas = self.gestor.listar_mascotas_cliente(cliente.id)
        print(f"\nMascotas de {cliente.nombre_completo}:\n")
        
        if not mascotas:
            print("No tiene mascotas registradas.")
        else:
            print("-" * 70)
            for m in mascotas:
                print(f"  {m}")
        self._pausa()
    
    def crear_mascota(self):
        """Registra una nueva mascota."""
        self._limpiar_pantalla()
        self._mostrar_titulo("REGISTRAR MASCOTA")
        
        cliente = self._seleccionar_cliente()
        if not cliente:
            self._pausa()
            return
        
        mascota = self._ingresar_mascota()
        try:
            mascota_id = self.gestor.crear_mascota(cliente.id, mascota)
            print(f"\nMascota registrada con ID: {mascota_id}")
            print(f"   Para: {cliente.nombre_completo}")
        except Exception as e:
            print(f"\nError al registrar mascota: {e}")
        self._pausa()
    
    def editar_mascota(self):
        """Edita una mascota existente."""
        self._limpiar_pantalla()
        self._mostrar_titulo("EDITAR MASCOTA")
        
        cliente = self._seleccionar_cliente()
        if not cliente:
            self._pausa()
            return
        
        mascotas = self.gestor.listar_mascotas_cliente(cliente.id)
        if not mascotas:
            print(f"\n{cliente.nombre_completo} no tiene mascotas.")
            self._pausa()
            return
        
        print(f"\nMascotas de {cliente.nombre_completo}:")
        for i, m in enumerate(mascotas, 1):
            print(f"  {i}. {m}")
        
        try:
            opcion = int(input("\nSeleccione numero: "))
            if not (1 <= opcion <= len(mascotas)):
                raise ValueError
            mascota = mascotas[opcion - 1]
        except ValueError:
            print("Seleccion invalida.")
            self._pausa()
            return
        
        print(f"\nEditando: {mascota.nombre}")
        print("(Deje vacio para mantener el valor actual)")
        
        nombre = input(f"Nombre [{mascota.nombre}]: ").strip()
        if nombre:
            mascota.nombre = nombre
        
        raza = input(f"Raza [{mascota._raza}]: ").strip()
        if raza:
            mascota._raza = raza
        
        fecha_nac = input(f"Fecha nac. [{mascota._fecha_nac}]: ").strip()
        if fecha_nac:
            mascota._fecha_nac = fecha_nac
        
        color = input(f"Color [{mascota._color}]: ").strip()
        if color:
            mascota._color = color
        
        peso = input(f"Peso [{mascota._peso_kg}]: ").strip()
        if peso:
            mascota._peso_kg = float(peso) if peso else None
        
        try:
            if self.gestor.actualizar_mascota(mascota):
                print("\nMascota actualizada correctamente.")
            else:
                print("\nError al actualizar mascota.")
        except Exception as e:
            print(f"\nError: {e}")
        self._pausa()
    
    def eliminar_mascota(self):
        """Elimina una mascota."""
        self._limpiar_pantalla()
        self._mostrar_titulo("ELIMINAR MASCOTA")
        
        cliente = self._seleccionar_cliente()
        if not cliente:
            self._pausa()
            return
        
        mascotas = self.gestor.listar_mascotas_cliente(cliente.id)
        if not mascotas:
            print(f"\n{cliente.nombre_completo} no tiene mascotas.")
            self._pausa()
            return
        
        print(f"\nMascotas de {cliente.nombre_completo}:")
        for i, m in enumerate(mascotas, 1):
            print(f"  {i}. {m}")
        
        try:
            opcion = int(input("\nSeleccione numero: "))
            if not (1 <= opcion <= len(mascotas)):
                raise ValueError
            mascota = mascotas[opcion - 1]
        except ValueError:
            print("Seleccion invalida.")
            self._pausa()
            return
        
        print(f"\nEliminar a {mascota.nombre}?")
        confirmar = input("   Confirmar (s/N): ").lower()
        
        if confirmar == 's':
            if self.gestor.eliminar_mascota(mascota.id):
                print("\nMascota eliminada correctamente.")
            else:
                print("\nError al eliminar mascota.")
        else:
            print("\nOperacion cancelada.")
        self._pausa()
    
    def ver_info_mascota(self):
        """Muestra informacion completa de una mascota incluyendo polimorfismo."""
        self._limpiar_pantalla()
        self._mostrar_titulo("INFORMACION COMPLETA DE MASCOTA")
        
        cliente = self._seleccionar_cliente()
        if not cliente:
            self._pausa()
            return
        
        mascotas = self.gestor.listar_mascotas_cliente(cliente.id)
        if not mascotas:
            print(f"\n{cliente.nombre_completo} no tiene mascotas.")
            self._pausa()
            return
        
        print(f"\nMascotas de {cliente.nombre_completo}:")
        for i, m in enumerate(mascotas, 1):
            print(f"  {i}. {m}")
        
        try:
            opcion = int(input("\nSeleccione numero: "))
            if not (1 <= opcion <= len(mascotas)):
                raise ValueError
            mascota = mascotas[opcion - 1]
        except ValueError:
            print("Seleccion invalida.")
            self._pausa()
            return
        
        print(f"\nInformacion de {mascota.nombre}:")
        print("-" * 50)
        print(f"  ID: {mascota.id}")
        print(f"  Nombre: {mascota.nombre}")
        print(f"  Especie: {mascota.especie}")
        print(f"  Raza: {mascota._raza or 'No especificada'}")
        print(f"  Color: {mascota._color or 'No especificado'}")
        print(f"  Peso: {mascota._peso_kg or 'No registrado'} kg")
        print(f"  Propietario: {mascota.nombre_cliente}")
        
        # Demostracion de polimorfismo
        print("\n--- Polimorfismo en accion ---")
        try:
            info_completa = self.gestor.obtener_info_completa_mascota(mascota.id)
            print(f"  Descripcion: {info_completa}")
            print("\n  Nota: El metodo 'obtener_descripcion_completa()' se comporta")
            print("  de manera diferente segun la especie de la mascota.")
            print("  Esto demuestra el polimorfismo en el diseno.")
        except Exception as e:
            print(f"  Error al obtener informacion: {e}")
        
        self._pausa()
    
    def menu_buscar(self):
        """Menu de busqueda."""
        self._limpiar_pantalla()
        self._mostrar_titulo("BUSQUEDA")
        
        termino = input("\nIngrese termino de busqueda: ").strip()
        if not termino:
            print("Ingrese un termino valido.")
            self._pausa()
            return
        
        print("\n" + "=" * 50)
        print("  CLIENTES ENCONTRADOS")
        print("=" * 50)
        
        clientes = self.gestor.buscar_cliente(termino)
        if clientes:
            print(f"\n{len(clientes)} cliente(s):")
            for c in clientes:
                print(f"  {c}")
        else:
            print("\nNo se encontraron clientes.")
        
        print("\n" + "=" * 50)
        print("  MASCOTAS ENCONTRADAS")
        print("=" * 50)
        
        mascotas = self.gestor.buscar_mascota(termino)
        if mascotas:
            print(f"\n{len(mascotas)} mascota(s):")
            for m in mascotas:
                print(f"  {m['nombre']} ({m['especie']}) - Propietario: {m['propietario']}")
        else:
            print("\nNo se encontraron mascotas.")
        
        self._pausa()