from app.models.database import get_db, close_db
from datetime import datetime

def adicionar_transacao(tipo, valor, categoria_id, data, descricao):
    con = get_db()
    try:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO transacoes (tipo, valor, categoria_id, data, descricao)
            VALUES (%s, %s, %s, %s, %s)
        """, (tipo, valor, categoria_id, data, descricao))
        con.commit()
    finally:
        cur.close()
        close_db(con)

def listar_transacoes():
    con = get_db()
    try:
        cur = con.cursor()
        cur.execute("""
            SELECT t.id, t.tipo, t.valor, c.nome, t.data, t.descricao
            FROM transacoes t
            JOIN categorias c ON t.categoria_id = c.id
            ORDER BY t.data DESC
        """)
        transacoes = cur.fetchall()
        return transacoes
    finally:
        cur.close()
        close_db(con)

def listar_transacoes_filtradas(tipo=None, categoria_id=None, data_inicio=None, data_fim=None, busca=None, page=1, per_page=10):
    con = get_db()
    try:
        cur = con.cursor()
        
        # Base query
        query = """
            SELECT t.id, t.tipo, t.valor, c.nome, t.data, t.descricao
            FROM transacoes t
            JOIN categorias c ON t.categoria_id = c.id
            WHERE 1=1
        """
        params = []
        
        # Aplicar filtros
        if tipo:
            query += " AND t.tipo = %s"
            params.append(tipo)
        
        if categoria_id:
            query += " AND t.categoria_id = %s"
            params.append(categoria_id)
        
        if data_inicio:
            query += " AND TO_DATE(t.data, 'DD/MM/YYYY') >= TO_DATE(%s, 'YYYY-MM-DD')"
            params.append(data_inicio)
        
        if data_fim:
            query += " AND TO_DATE(t.data, 'DD/MM/YYYY') <= TO_DATE(%s, 'YYYY-MM-DD')"
            params.append(data_fim)
        
        if busca:
            query += " AND (t.descricao ILIKE %s OR c.nome ILIKE %s)"
            params.extend([f"%{busca}%", f"%{busca}%"])
        
        # Contar total de registros
        count_query = f"SELECT COUNT(*) FROM ({query}) as subquery"
        cur.execute(count_query, params)
        total = cur.fetchone()[0]
        
        # Adicionar ordenação e paginação
        query += " ORDER BY t.data DESC LIMIT %s OFFSET %s"
        params.extend([per_page, (page - 1) * per_page])
        
        cur.execute(query, params)
        transacoes = cur.fetchall()
        
        return transacoes, total
    finally:
        cur.close()
        close_db(con)

def obter_transacao_por_id(transacao_id):
    con = get_db()
    try:
        cur = con.cursor()
        cur.execute("""
            SELECT t.id, t.tipo, t.valor, t.categoria_id, c.nome, t.data, t.descricao
            FROM transacoes t
            JOIN categorias c ON t.categoria_id = c.id
            WHERE t.id = %s
        """, (transacao_id,))
        transacao = cur.fetchone()
        return transacao
    finally:
        cur.close()
        close_db(con)

def editar_transacao(transacao_id, tipo, valor, categoria_id, data, descricao):
    con = get_db()
    try:
        cur = con.cursor()
        cur.execute("""
            UPDATE transacoes
            SET tipo = %s, valor = %s, categoria_id = %s, data = %s, descricao = %s
            WHERE id = %s
        """, (tipo, valor, categoria_id, data, descricao, transacao_id))
        con.commit()
    finally:
        cur.close()
        close_db(con)

def deletar_transacao(transacao_id):
    con = get_db()
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM transacoes WHERE id = %s", (transacao_id,))
        con.commit()
    finally:
        cur.close()
        close_db(con)
