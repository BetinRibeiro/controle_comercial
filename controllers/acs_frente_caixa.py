# -*- coding: utf-8 -*-
def marcar_produto_operacao_como_finalizado():
    # Consulta para obter todas as entradas em produto_operacao com operação ativa
    operacoes_ativas = db(db.operacao.ativo == True).select(db.operacao.id)

    # Atualiza todas as entradas em produto_operacao relacionadas às operações ativas
    for operacao in operacoes_ativas:
        db((db.produto_operacao.operacao == operacao.id) &
           (db.produto_operacao.finalizado == False)).update(finalizado=True)
    return True

@auth.requires_login()
def index():
#     response.view = 'generic.html'  # use a generic view
    """
    Página de operações do usuário logado.

    Essa função exibe uma página onde o usuário pode realizar operações,
    incluindo a adição de produtos às operações inativas. A função também
    exibe os produtos adicionados à operação atual.

    Returns:
        dict: Um dicionário contendo informações para a página HTML.
            - operacao: Objeto de operação inativa do usuário logado.
            - form: Formulário para adicionar produtos à operação.
            - produto: Produto encontrado pelo código de barras.
            - msn: Mensagem de aviso se o produto não estiver cadastrado.
            - rows: Produtos adicionados à operação atual.
    """
    tipo=request.args(0, cast=str)
    operacao = consultar_ultima_operacao_inativa(auth.user.id,tipo)
    form = None
    produto=None
    msn= None
    if len(request.args) == 2:
        produto = db(db.produto.codigo_barras==request.args(1, cast=str)).select().first()
        if produto:
            db.produto_operacao.operacao.default = operacao.id
            db.produto_operacao.produto.default = produto.id
            if 'compra' in tipo:
                db.produto_operacao.tipo_movimentacao.default='entrada'
                db.produto_operacao.custo_unitario.writable=True
                db.produto_operacao.preco_unitario.writable=True
            elif 'venda' in tipo:
                db.produto_operacao.tipo_movimentacao.default='saida'
                if produto.preco_unitario<=0:
                    redirect(URL('index',args=tipo))
#                     msn="Produto sem Preço"
            db.produto_operacao.custo_unitario.default = produto.custo_unitario
            db.produto_operacao.preco_unitario.default = produto.preco_unitario
            form = SQLFORM(db.produto_operacao).process()
            if form.accepted:
                redirect(URL('index',args=tipo))
            elif form.errors:
                response.flash = 'Formulário não aceito'
        else:
            msn= "Produto não cadastrado"
    rows=[]
    if operacao:
        rows = db(db.produto_operacao.operacao==operacao.id).select()
    return locals()

def consultar_ultima_operacao_inativa(usuario_id,tipo):
    """
    Consulta a última operação inativa de um usuário.

    Esta função realiza uma busca no banco de dados para encontrar a última
    operação inativa associada a um usuário específico.

    Args:
        usuario_id (int): O ID do usuário para o qual a operação será consultada.

    Returns:
        operacao (Row) or None: Um objeto Row representando a última operação inativa
            do usuário. Retorna None se nenhuma operação inativa for encontrada.
    """
    # Consulta a última operação inativa do usuário
    operacao = db((db.operacao.created_by == usuario_id) &
                  (db.operacao.ativo == False) &
                  (db.operacao.tipo == tipo)).select(
                      orderby=~db.operacao.id, limitby=(0, 1)).first()

    if operacao:
        return operacao
    else:
        return None

def buscar_ultima_operacao(usuario_id):
    """
    Busca a última operação criada por um usuário e retorna o próximo ID disponível.

    Esta função consulta o banco de dados para encontrar a última operação criada pelo
    usuário especificado e retorna o próximo ID disponível para criar uma nova operação.

    Args:
        usuario_id (int): O ID do usuário para o qual a operação será buscada.

    Returns:
        int: O próximo ID disponível para criar uma nova operação. Se nenhuma operação
            for encontrada, retorna 1.
    """
    # Define a query para buscar a última operação do usuário
    query = (db.operacao.created_by == usuario_id)

    # Consulta a última operação do usuário
    ultima_operacao = db(query).select(db.operacao.id, orderby=~db.operacao.id, limitby=(0, 1)).first()

    if ultima_operacao:
        return ultima_operacao.id+1
    else:
        return 1



def criar_operacao(empresa_id,tipo,codigo,pessoa_id=None):
    """
    Cria uma nova operação no banco de dados.

    Esta função cria uma nova entrada de operação no banco de dados, associando-a com os parâmetros fornecidos.

    Args:
        empresa_id (int): O ID da empresa relacionada à operação.
        tipo (str): O tipo de operação, por exemplo, "compra" ou "venda".
        codigo (str): O código da operação.
        pessoa_id (int, opcional): O ID da pessoa relacionada à operação, se aplicável.

    Returns:
        int or None: O ID da operação criada no banco de dados, ou None se a criação falhar.
    """
    ativo = False  # Substitua pelo valor desejado
    operacao_id = db.operacao.insert(
        empresa=empresa_id,
        pessoa=pessoa_id,
        codigo=codigo,
        tipo=tipo,
        valor_total=0,
        custo_total=0,
        ativo=ativo
    )
    if operacao_id:
        return operacao_id
    else:
        return None

@auth.requires_login()
def abrir_operacao():
    """
    Abre uma nova operação para o usuário logado.

    Esta função cria uma nova operação no banco de dados com base nas informações
    do usuário logado e nos argumentos da URL. Ela gera um código de operação, consulta
    o ID da última operação criada pelo usuário e redireciona para a página inicial.

    Returns:
        dict: Um dicionário com as informações locais para a renderização da página.
            O redirecionamento ocorre dentro da função.
    """
    # Define a view a ser usada
    response.view = 'generic.html'  # use a generic view
    tipo = request.args(0)
    id_ultima_operacao = buscar_ultima_operacao(auth.user.id)
    codigo = gerar_codigo(request.now,auth.user.id,id_ultima_operacao)

    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    criar_operacao(empresa.id,tipo,codigo)
    redirect(URL('index',args=tipo))
    return locals()

def fechar_operacao():
    """
    Fecha uma operação específica.

    Esta função recebe o ID da operação como argumento da URL e atualiza o status
    da operação para "ativo=True", indicando que a operação foi fechada. Em seguida,
    redireciona o usuário de volta para a página inicial.

    Returns:
        None: A função não retorna nenhum valor, mas realiza a atualização e o redirecionamento.
    """
    # Obtém o ID da operação a partir dos argumentos da URL
    operacao = db.operacao(request.args(0, cast=int))
    operacao.ativo=True
    tipo = operacao.tipo
    operacao.update_record()
     # Atualiza os estoques e preços de custo dos produtos relacionados a essa operação
    produto_operacoes = db(db.produto_operacao.operacao == operacao.id).select()

    for produto_op in produto_operacoes:
        atualizar_estoque_produto(produto_op.produto)
    marcar_produto_operacao_como_finalizado()
    redirect(URL('index',args=tipo))

def cancelar_operacao():
    """
    Cancela uma operação específica.

    Esta função recebe o ID da operação como argumento da URL e realiza a exclusão
    da operação no banco de dados. Após a exclusão, redireciona o usuário de volta
    para a página inicial.

    Returns:
        None: A função não retorna nenhum valor, mas realiza a exclusão e o redirecionamento.
    """
    # Obtém o ID da operação a partir dos argumentos da URL
    tipo = db.operacao(request.args(0, cast=int)).tipo
    db(db.operacao.id==request.args(0, cast=int)).delete()
    redirect(URL('index',args=tipo))
    return True

def definir_pessoa():
    operacao = db.operacao(request.args(0, cast=int))
    tipo = operacao.tipo
    tipo_pessoa= 'fornecedor'
    if tipo=='compra':
        tipo_pessoa= 'cliente'
    response.view = 'generic.html'  # use a generic view
    request.function = 'Alterar produto'
    db.operacao.pessoa.writable=True
    db.operacao.pessoa.readable=True
    db.operacao.pessoa.requires=IS_IN_DB(db((db.pessoa.empresa == operacao.empresa) & (db.pessoa.tipo == tipo_pessoa)), 'pessoa.id', '%(nome)s')

    # Cria e processa o formulário de alteração
    form = SQLFORM(db.operacao, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        redirect(URL('index',args=tipo))
    elif form.errors:
        response.flash = 'Formulário não aceito'
    # Retorna o formulário para a visualização
    return dict(form=form)


def retirar_item():
    response.view = 'generic.html'  # use a generic view
    produto_operacao = db.produto_operacao(request.args(0, cast=int))
    if produto_operacao:
        operacao = db.operacao(produto_operacao.operacao)
        db(db.produto_operacao.id==produto_operacao.id).delete()
        redirect(URL('index',args=operacao.tipo))
    return locals()
