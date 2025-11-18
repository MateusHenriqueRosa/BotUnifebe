import logging
from database.connection import get_connection, get_cursor_dict
import bcrypt

try:
    HAS_BCRYPT = True
except Exception:
    bcrypt = None
    HAS_BCRYPT = False
    logging.warning(
        "bcrypt não encontrado. Instale 'bcrypt' para hashing seguro de senhas."
    )


def hash_senha(password: str) -> str:
    if HAS_BCRYPT:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")
    else:
        return password


def conferir_senha(password: str, stored_hash: str) -> bool:
    if HAS_BCRYPT:
        try:
            return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))
        except Exception:
            return False
    else:
        return password == stored_hash


def criar_usuario(username: str, email: str, password: str) -> dict:
    conn = None
    try:
        conn = get_connection()
        cur = get_cursor_dict(conn)
        password_hash = hash_senha(password)
        cur.execute(
            """
            INSERT INTO usuarios (username, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id, username, email, created_at
            """,
            (username, email, password_hash),
        )
        usuario = cur.fetchone()
        conn.commit()
        cur.close()
        return usuario

    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Erro ao criar usuário: {e}")
        raise
    finally:
        if conn:
            conn.close()


def buscar_usuario_por_username(username: str) -> dict:
    conn = None
    try:
        conn = get_connection()
        cur = get_cursor_dict(conn)
        cur.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        usuario = cur.fetchone()
        cur.close()
        return usuario
    except Exception as e:
        logging.error(f"Erro ao buscar usuário: {e}")
        raise
    finally:
        if conn:
            conn.close()


def validar_login(username: str, password: str) -> bool:
    usuario = buscar_usuario_por_username(username)
    if not usuario:
        return False
    stored_hash = usuario.get("password_hash")
    return conferir_senha(password, stored_hash)
