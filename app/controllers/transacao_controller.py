from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app.models.transacao_model import *
from app.models.categoria_model import listar_categorias
import math

transacao_bp = Blueprint('transacao', __name__)

@transacao_bp.route('/')
def index():
    # Parâmetros de filtro
    tipo = request.args.get('tipo')
    categoria_id = request.args.get('categoria_id')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    busca = request.args.get('busca')
    page = int(request.args.get('page', 1))
    per_page = 10
    
    # Buscar transações filtradas
    transacoes, total = listar_transacoes_filtradas(
        tipo=tipo,
        categoria_id=categoria_id,
        data_inicio=data_inicio,
        data_fim=data_fim,
        busca=busca,
        page=page,
        per_page=per_page
    )
    
    # Calcular paginação
    total_pages = math.ceil(total / per_page)
    
    # Buscar categorias para o filtro
    categorias = listar_categorias()
    
    return render_template('index.html', 
                         transacoes=transacoes,
                         categorias=categorias,
                         current_page=page,
                         total_pages=total_pages,
                         total=total,
                         filtros={
                             'tipo': tipo,
                             'categoria_id': categoria_id,
                             'data_inicio': data_inicio,
                             'data_fim': data_fim,
                             'busca': busca
                         })

@transacao_bp.route('/nova_transacao')
def nova_transacao():
    categorias = listar_categorias()
    return render_template('nova_transacao.html', categorias=categorias)

@transacao_bp.route('/adicionar_transacao', methods=['POST'])
def adicionar_transacao_route():
    try:
        # Validações
        tipo = request.form.get('tipo', '').strip()
        if not tipo or tipo not in ['receita', 'saida']:
            raise ValueError("Tipo de transação inválido.")
        if tipo == 'saida':
            tipo = 'despesa'
        
        valor_str = request.form.get('valor', '').strip()
        if not valor_str:
            raise ValueError("Valor é obrigatório.")
        try:
            valor = float(valor_str.replace(',', '.'))
            if valor <= 0:
                raise ValueError("Valor deve ser positivo.")
        except ValueError:
            raise ValueError("Valor inválido.")
        
        categoria_id_str = request.form.get('categoria_id', '').strip()
        if not categoria_id_str:
            raise ValueError("Categoria é obrigatória.")
        try:
            categoria_id = int(categoria_id_str)
        except ValueError:
            raise ValueError("Categoria inválida.")
        
        data_americana = request.form.get('data', '').strip()
        if not data_americana:
            raise ValueError("Data é obrigatória.")
        try:
            data = datetime.strptime(data_americana, '%Y-%m-%d').strftime('%d-%m-%Y')
        except ValueError:
            raise ValueError("Data inválida.")
        
        descricao = request.form.get('descricao', '').strip()
        if len(descricao) > 500:
            raise ValueError("Descrição muito longa (máximo 500 caracteres).")
        
        adicionar_transacao(tipo, valor, categoria_id, data, descricao)
        flash('Transação adicionada com sucesso!', 'success')
    except ValueError as e:
        flash(f'Erro de validação: {e}', 'error')
    except Exception as e:
        flash(f'Erro inesperado: {e}', 'error')
    
    return redirect(url_for('transacao.index'))

@transacao_bp.route('/editar_transacao/<int:transacao_id>')
def editar_transacao_form(transacao_id):
    transacao = obter_transacao_por_id(transacao_id)
    categorias = listar_categorias()
    return render_template('editar_transacao.html', transacao=transacao, categorias=categorias)

@transacao_bp.route('/atualizar_transacao/<int:transacao_id>', methods=['POST'])
def atualizar_transacao_route(transacao_id):
    try:
        # Validações
        tipo = request.form.get('tipo', '').strip()
        if not tipo or tipo not in ['receita', 'saida']:
            raise ValueError("Tipo de transação inválido.")
        if tipo == 'saida':
            tipo = 'despesa'
        
        valor_str = request.form.get('valor', '').strip()
        if not valor_str:
            raise ValueError("Valor é obrigatório.")
        try:
            valor = float(valor_str.replace(',', '.'))
            if valor <= 0:
                raise ValueError("Valor deve ser positivo.")
        except ValueError:
            raise ValueError("Valor inválido.")
        
        categoria_id_str = request.form.get('categoria_id', '').strip()
        if not categoria_id_str:
            raise ValueError("Categoria é obrigatória.")
        try:
            categoria_id = int(categoria_id_str)
        except ValueError:
            raise ValueError("Categoria inválida.")
        
        data_americana = request.form.get('data', '').strip()
        if not data_americana:
            raise ValueError("Data é obrigatória.")
        try:
            data = datetime.strptime(data_americana, '%Y-%m-%d').strftime('%d-%m-%Y')
        except ValueError:
            raise ValueError("Data inválida.")
        
        descricao = request.form.get('descricao', '').strip()
        if len(descricao) > 500:
            raise ValueError("Descrição muito longa (máximo 500 caracteres).")
        
        editar_transacao(transacao_id, tipo, valor, categoria_id, data, descricao)
        flash('Transação atualizada com sucesso!', 'success')
    except ValueError as e:
        flash(f'Erro de validação: {e}', 'error')
    except Exception as e:
        flash(f'Erro inesperado: {e}', 'error')
    
    return redirect(url_for('transacao.index'))

@transacao_bp.route('/deletar_transacao/<int:transacao_id>', methods=['POST'])
def deletar_transacao_route(transacao_id):
    try:
        deletar_transacao(transacao_id)
        flash('Transação deletada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro: {e}', 'error')
    
    return redirect(url_for('transacao.index'))