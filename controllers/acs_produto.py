import random

def gerar_numero_aleatorio(num1,num2):
    return random.randint(num1, num2)


# Página principal que lista produtos da empresa do usuário logado
@auth.requires_login()
def index():
#     db.produtosasafd.truncate('RESTART IDENTITY CASCADE')
    # Busca o usuário e empresa relacionada
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    # Redireciona para a página inicial se o usuário estiver inativo
    if usuario.ativo == False:
        redirect(URL('default', 'index'))

    # Configurações de paginação e verificação dos parâmetros da URL
    paginacao = empresa.paginacao
    if len(request.args) == 0:
        pagina = 1
    else:
        try:
            pagina = int(request.args[0])
        except ValueError:
            redirect(URL(args=[1]))
    
    # Lógica de cálculo de páginas e limites
    if pagina <= 0:
        pagina = 1
    total = db((db.produto.empresa == empresa.id)).count()
    paginas = total // paginacao
    if total % paginacao:
        paginas += 1
    if total == 0:
        paginas = 1
    if pagina > paginas:
        redirect(URL(args=[paginas]))

    limites = (paginacao * (pagina - 1), (paginacao * pagina))
    
    # Consulta os registros dos produtos da empresa, incluindo filtro de pesquisa
    registros = db((db.produto.empresa == empresa.id)).select(
        limitby=limites, orderby=~db.produto.id | db.produto.descricao)
    consul = request.args(1)
    if consul:
        registros = db((db.produto.empresa == empresa.id) & (
            (db.produto.descricao.contains(consul)) | (db.produto.codigo_barras.contains(consul)))).select(
            limitby=limites, orderby=db.produto.descricao)
    
    # Retorna os dados para a visualização
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa)


# Página de cadastro de produtos
@auth.requires_login()
def cadastrar():
    # Busca o usuário e empresa relacionada
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # use a generic view
    request.function = 'Cadastro de produto'

    # Define o valor padrão da empresa no formulário e processa o formulário
    db.produto.empresa.default = usuario.empresa
    if auth.user.id==1:
        db.produto.descricao.default = f'Produto {gerar_numero_aleatorio(1000,9999)}'
        db.produto.custo_unitario.default = gerar_numero_aleatorio(10,99)
    form = SQLFORM(db.produto).process()

    # Redireciona para a página principal após aceitar o formulário
    if form.accepted:
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Formulário não aceito'
    
    # Retorna o formulário para a visualização
    return dict(form=form)


# Página de alteração de produtos
@auth.requires_login()
def alterar():
    # Busca o usuário e produto relacionado
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    produto = db.produto(request.args(0, cast=int))

    if len(request.args) == 1:
        pagina = 1
    else:
        pagina = int(request.args[1])

    # Redireciona se o produto não pertencer à empresa do usuário
    if produto.empresa != usuario.empresa:
        redirect(URL('index'))
    
    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # use a generic view
    request.function = 'Alterar produto'

    # Cria e processa o formulário de alteração
    form = SQLFORM(db.produto, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        redirect(URL('index',args=pagina))
    elif form.errors:
        response.flash = 'Formulário não aceito'
    
    # Retorna o formulário para a visualização
    return dict(form=form)

@auth.requires_login()
def acessar():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    if usuario.ativo == False:
        redirect(URL('default', 'index'))

    produto = db.produto(request.args(0, cast=int))
    paginacao = empresa.paginacao
    if len(request.args) == 1:
        pagina = 1
    else:
        try:
            pagina = int(request.args[1])
        except ValueError:
            redirect(URL(args=[produto.id,1]))
    
    if pagina <= 0:
        pagina = 1
    total = db((db.produto_operacao.produto == produto.id)).count()
    paginas = total // paginacao
    if total % paginacao:
        paginas += 1
    if total == 0:
        paginas = 1
    if pagina > paginas:
        redirect(URL(args=[produto.id,paginas]))
    if len(request.args) == 1:
        redirect(URL(args=[produto.id,paginas]))

    limites = (paginacao * (pagina - 1), (paginacao * pagina))
    
    registros = db((db.produto_operacao.produto == produto.id)).select(
        limitby=limites, orderby=db.produto_operacao.id | db.produto_operacao.produto)
    
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa,produto=produto)
