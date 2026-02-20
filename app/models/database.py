import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
import os
from dotenv import load_dotenv

load_dotenv()

# Connection pool para melhor performance
_db_pool = None

def get_db_pool():
    global _db_pool
    if _db_pool is None:
        conninfo = f"host={os.getenv('DB_HOST', 'localhost')} port={os.getenv('DB_PORT', '5432')} dbname={os.getenv('DB_NAME', 'financas_db')} user={os.getenv('DB_USER', 'username')} password={os.getenv('DB_PASSWORD', 'password')}"
        _db_pool = ConnectionPool(conninfo, min_size=1, max_size=10)
    return _db_pool

def get_db():
    """
    Retorna uma conexão do pool.

    :return: conexão psycopg
    """
    try:
        pool = get_db_pool()
        conn = pool.getconn()
        return conn
    except psycopg.Error as e:
        raise Exception(f"Erro ao conectar ao banco de dados: {e}")

def close_db(conn):
    """
    Retorna a conexão ao pool.
    """
    if conn:
        pool = get_db_pool()
        pool.putconn(conn)