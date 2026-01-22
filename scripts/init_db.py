import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_tables():
    """
    Cria as tabelas necessárias no banco PostgreSQL
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'financas_db'),
            user=os.getenv('DB_USER', 'username'),
            password=os.getenv('DB_PASSWORD', 'password')
        )
        
        cur = conn.cursor()
        
        # Criar tabela categorias
        cur.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL UNIQUE
            )
        """)
        
        # Criar tabela transacoes
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transacoes (
                id SERIAL PRIMARY KEY,
                tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('receita', 'despesa')),
                valor DECIMAL(10,2) NOT NULL,
                categoria_id INTEGER REFERENCES categorias(id),
                data VARCHAR(10) NOT NULL,
                descricao TEXT
            )
        """)
        
        # Inserir categorias padrão se não existirem
        cur.execute("SELECT COUNT(*) FROM categorias")
        if cur.fetchone()[0] == 0:
            categorias_padrao = [
                ('Alimentação',),
                ('Transporte',),
                ('Moradia',),
                ('Saúde',),
                ('Educação',),
                ('Lazer',),
                ('Salário',),
                ('Freelance',),
                ('Investimentos',)
            ]
            cur.executemany("INSERT INTO categorias (nome) VALUES (%s)", categorias_padrao)
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("Tabelas criadas com sucesso!")
        
    except psycopg2.Error as e:
        print(f"Erro ao criar tabelas: {e}")

if __name__ == "__main__":
    create_tables()