"""
database.py - Capa de acceso a datos SQLite para VetApp (version consola)
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "vetapp.db"

def get_conn() -> sqlite3.Connection:
    """Obtiene una conexion a la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos con las tablas necesarias."""
    with get_conn() as conn:
        conn.executescript("""
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS cliente (
            id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT    NOT NULL,
            apellido    TEXT    NOT NULL,
            dni         TEXT    UNIQUE,
            telefono    TEXT,
            email       TEXT,
            direccion   TEXT,
            activo      INTEGER NOT NULL DEFAULT 1,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS mascota (
            id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            cliente_id  INTEGER NOT NULL,
            nombre      TEXT    NOT NULL,
            especie     TEXT    NOT NULL,
            raza        TEXT,
            fecha_nac   TEXT,
            sexo        TEXT    NOT NULL DEFAULT 'desconocido'
                                CHECK (sexo IN ('M','F','desconocido')),
            peso_kg     REAL,
            color       TEXT,
            castrado    INTEGER NOT NULL DEFAULT 0,
            activo      INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (cliente_id) REFERENCES cliente(id)
        );

        INSERT OR IGNORE INTO cliente (nombre, apellido, dni, telefono, email) 
        VALUES 
            ('Carlos', 'Fernandez', '30111222', '1155551111', 'carlos@mail.com'),
            ('Ana', 'Lopez', '27333444', '1155552222', 'ana@mail.com');
        
        INSERT OR IGNORE INTO mascota (cliente_id, nombre, especie, raza, fecha_nac, sexo, peso_kg, color, castrado)
        VALUES 
            (1, 'Toby', 'Perro', 'Labrador', '2019-03-15', 'M', 28.5, 'Amarillo', 1),
            (1, 'Mimi', 'Gato', 'Siames', '2021-07-20', 'F', 3.8, 'Blanco', 0),
            (2, 'Rocky', 'Perro', 'Bulldog Frances', '2020-11-05', 'M', 12.0, 'Atigrado', 1);
        """)


def get_clientes() -> list[dict]:
    """Obtiene todos los clientes activos con conteo de mascotas."""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT c.*, COUNT(m.id) AS cant_mascotas
            FROM cliente c
            LEFT JOIN mascota m ON m.cliente_id = c.id AND m.activo = 1
            WHERE c.activo = 1
            GROUP BY c.id
            ORDER BY c.apellido, c.nombre
        """).fetchall()
        return [dict(r) for r in rows]

def get_cliente(cliente_id: int) -> dict | None:
    """Obtiene un cliente por su ID."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM cliente WHERE id = ? AND activo = 1", 
            (cliente_id,)
        ).fetchone()
        return dict(row) if row else None

def buscar_cliente(termino: str) -> list[dict]:
    """Busca clientes por nombre o apellido."""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT c.*, COUNT(m.id) AS cant_mascotas
            FROM cliente c
            LEFT JOIN mascota m ON m.cliente_id = c.id AND m.activo = 1
            WHERE c.activo = 1 
            AND (c.nombre LIKE ? OR c.apellido LIKE ?)
            GROUP BY c.id
            ORDER BY c.apellido, c.nombre
        """, (f'%{termino}%', f'%{termino}%')).fetchall()
        return [dict(r) for r in rows]

def crear_cliente(data: dict) -> int:
    """Crea un nuevo cliente."""
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO cliente (nombre, apellido, dni, telefono, email, direccion)
            VALUES (?,?,?,?,?,?)
        """, (
            data["nombre"].strip(),
            data["apellido"].strip(),
            data.get("dni", "").strip() or None,
            data.get("telefono", "").strip() or None,
            data.get("email", "").strip() or None,
            data.get("direccion", "").strip() or None,
        ))
        return cur.lastrowid

def actualizar_cliente(cliente_id: int, data: dict):
    """Actualiza un cliente existente."""
    with get_conn() as conn:
        conn.execute("""
            UPDATE cliente
            SET nombre=?, apellido=?, dni=?, telefono=?, email=?, direccion=?
            WHERE id=? AND activo = 1
        """, (
            data["nombre"].strip(),
            data["apellido"].strip(),
            data.get("dni", "").strip() or None,
            data.get("telefono", "").strip() or None,
            data.get("email", "").strip() or None,
            data.get("direccion", "").strip() or None,
            cliente_id,
        ))

def eliminar_cliente(cliente_id: int) -> bool:
    """Elimina logicamente un cliente (lo desactiva)."""
    with get_conn() as conn:
        mascotas = conn.execute(
            "SELECT COUNT(*) FROM mascota WHERE cliente_id = ? AND activo = 1",
            (cliente_id,)
        ).fetchone()[0]
        
        if mascotas > 0:
            return False
        
        conn.execute(
            "UPDATE cliente SET activo = 0 WHERE id = ?",
            (cliente_id,)
        )
        return True


def get_mascotas_cliente(cliente_id: int) -> list[dict]:
    """Obtiene todas las mascotas de un cliente."""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT * FROM mascota
            WHERE cliente_id = ? AND activo = 1
            ORDER BY nombre
        """, (cliente_id,)).fetchall()
        return [dict(r) for r in rows]

def get_mascota(mascota_id: int) -> dict | None:
    """Obtiene una mascota por su ID."""
    with get_conn() as conn:
        row = conn.execute("""
            SELECT m.*, c.nombre || ' ' || c.apellido AS propietario
            FROM mascota m
            JOIN cliente c ON c.id = m.cliente_id
            WHERE m.id = ? AND m.activo = 1
        """, (mascota_id,)).fetchone()
        return dict(row) if row else None

def buscar_mascota(termino: str) -> list[dict]:
    """Busca mascotas por nombre o por propietario."""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT m.*, 
                   c.nombre || ' ' || c.apellido AS propietario,
                   c.telefono
            FROM mascota m
            JOIN cliente c ON c.id = m.cliente_id
            WHERE m.activo = 1 
            AND (m.nombre LIKE ? OR c.nombre LIKE ? OR c.apellido LIKE ?)
            ORDER BY m.nombre
        """, (f'%{termino}%', f'%{termino}%', f'%{termino}%')).fetchall()
        return [dict(r) for r in rows]

def crear_mascota(data: dict) -> int:
    """Crea una nueva mascota."""
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO mascota
                (cliente_id, nombre, especie, raza, fecha_nac, sexo, peso_kg, color, castrado)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            data["cliente_id"],
            data["nombre"].strip(),
            data["especie"].strip(),
            data.get("raza", "").strip() or None,
            data.get("fecha_nac", "").strip() or None,
            data.get("sexo", "desconocido"),
            float(data["peso_kg"]) if data.get("peso_kg") and data["peso_kg"] else None,
            data.get("color", "").strip() or None,
            1 if data.get("castrado") else 0,
        ))
        return cur.lastrowid

def actualizar_mascota(mascota_id: int, data: dict):
    """Actualiza una mascota existente."""
    with get_conn() as conn:
        conn.execute("""
            UPDATE mascota
            SET nombre=?, especie=?, raza=?, fecha_nac=?,
                sexo=?, peso_kg=?, color=?, castrado=?
            WHERE id=? AND activo = 1
        """, (
            data["nombre"].strip(),
            data["especie"].strip(),
            data.get("raza", "").strip() or None,
            data.get("fecha_nac", "").strip() or None,
            data.get("sexo", "desconocido"),
            float(data["peso_kg"]) if data.get("peso_kg") and data["peso_kg"] else None,
            data.get("color", "").strip() or None,
            1 if data.get("castrado") else 0,
            mascota_id,
        ))

def eliminar_mascota(mascota_id: int) -> bool:
    """Elimina logicamente una mascota."""
    with get_conn() as conn:
        conn.execute(
            "UPDATE mascota SET activo = 0 WHERE id = ?",
            (mascota_id,)
        )
        return True
