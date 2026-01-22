# Importa os recursos necessários do Flask
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Importa apenas as funções necessárias do model de categoria
from app.models.categoria_model import listar_categorias, adicionar_categoria

# Cria um Blueprint para organizar as rotas relacionadas a categorias
# 'categoria' será usado no url_for()
categoria_bp = Blueprint('categoria', __name__)


# ROTA: LISTAR CATEGORIAS
@categoria_bp.route('/categorias')
def categorias():
    # Busca todas as categorias cadastradas no banco de dados
    categorias = listar_categorias()

    # Renderiza o template e envia a lista de categorias para o HTML
    return render_template('categorias.html', categorias=categorias)


# ROTA: ADICIONAR CATEGORIA
@categoria_bp.route('/adicionar_categoria', methods=['POST'])
def adicionar_categoria_route():
    # Captura o valor do campo "nome" enviado pelo formulário
    nome = request.form.get('nome', '').strip()

    # Validação: impede o cadastro de categorias vazias
    if not nome:
        flash('O nome da categoria não pode ser vazio.', 'error')
        return redirect(url_for('categoria.categorias'))

    try:
        adicionar_categoria(nome)

        flash('Categoria adicionada com sucesso!', 'success')

    except Exception as e:
        # Captura qualquer erro ocorrido durante a inserção
        # Exemplo: categoria duplicada
        flash(f'Erro ao adicionar categoria: {e}', 'error')

    # Redireciona de volta para a página de listagem de categorias
    return redirect(url_for('categoria.categorias'))
