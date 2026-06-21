"""
main.py - Punto de entrada a consola
"""
from database import init_db
from menu import MenuVetApp

def main():
    """Funcion principal."""
    print("Inicializando Alta de Clientes y Mascotas...")
    
    init_db()
    print("Base de datos lista.")
    
    app = MenuVetApp()
    app.mostrar_menu_principal()

if __name__ == "__main__":
    main()