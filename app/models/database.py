import psycopg2
import psycopg2.extras
import psycopg2.pool
import os
from dotenv import load_dotenv

load_dotenv()

# Connection pool para melhor performance
_db_pool = None

def get_db_pool():
    global _db_pool
    if _db_pool is None:
        _db_pool = psycopg2.pool.SimpleConnectionPool(
            1,  # min connections
            10,  # max connections
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'financas_db'),
            user=os.getenv('DB_USER', 'username'),
            password=os.getenv('DB_PASSWORD', 'password')
        )
    return _db_pool

def get_db():
    """
    Retorna uma conexão do pool.

    :return: conexão psycopg2
    """
    try:
        pool = get_db_pool()
        conn = pool.getconn()
        return conn
    except psycopg2.Error as e:
        raise Exception(f"Erro ao conectar ao banco de dados: {e}")

def close_db(conn):
    """
    Retorna a conexão ao pool.
    """
    if conn:
        pool = get_db_pool()
        pool.putconn(conn)
