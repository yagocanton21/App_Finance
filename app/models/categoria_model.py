from app.models.database import get_db, close_db


def adicionar_categoria(nome: str) -> None:
    """
    Adiciona uma nova categoria ao banco de dados.

    :param nome: Nome da categoria
    :raises ValueError: Se o nome estiver vazio
    """
    if not nome or not nome.strip():
        raise ValueError("O nome da categoria não pode ser vazio.")

    con = get_db()
    try:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO categorias (nome) VALUES (%s)",
            (nome.strip(),)
        )
        con.commit()
    finally:
        cur.close()
        close_db(con)

def listar_categorias():
    """
    Lista todas as categorias do banco de dados.
    
    :return: Lista de tuplas (id, nome)
    """
    con = get_db()
    try:
        cur = con.cursor()
        cur.execute("SELECT id, nome FROM categorias ORDER BY nome")
        categorias = cur.fetchall()
        return categorias
    finally:
        cur.close()
        close_db(con)