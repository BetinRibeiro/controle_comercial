# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
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
    total = db(db.registro_financeiro.operacao.belongs(
        db(db.operacao.empresa == empresa.id)._select(db.operacao.id)
    )).count()
    paginas = total // paginacao
    if total % paginacao:
        paginas += 1
    if total == 0:
        paginas = 1
    if pagina > paginas:
        redirect(URL(args=[paginas]))

    limites = (paginacao * (pagina - 1), (paginacao * pagina))

    # Consulta os registros financeiros das operações da empresa
    registros = db(db.registro_financeiro.operacao.belongs(
        db(db.operacao.empresa == empresa.id)._select(db.operacao.id)
    )).select(
        join=db.registro_financeiro.on(db.operacao.id == db.registro_financeiro.operacao),
        limitby=limites, orderby=~db.registro_financeiro.operacao | db.operacao.codigo)

    # Retorna os dados para a visualização
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa)


# Página de cadastro de registros financeiros
@auth.requires_login()
def cadastrar():
    # Busca o usuário e empresa relacionada
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # use a generic view
    request.function = 'Cadastro de registro financeiro'

    # Define o valor padrão da empresa no formulário e processa o formulário
    db.registro_financeiro.operacao.empresa.default = usuario.empresa
    form = SQLFORM(db.registro_financeiro).process()

    # Redireciona para a página principal após aceitar o formulário
    if form.accepted:
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Formulário não aceito'

    # Retorna o formulário para a visualização
    return dict(form=form)


# Página de alteração de registros financeiros
@auth.requires_login()
def alterar():
    # Busca o usuário e registro financeiro relacionado
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    registro_financeiro = db.registro_financeiro(request.args(0, cast=int))

    if len(request.args) == 1:
        pagina = 1
    else:
        pagina = int(request.args[1])

    # Redireciona se o registro financeiro não pertencer à empresa do usuário
    if registro_financeiro.operacao.empresa != usuario.empresa:
        redirect(URL('index'))

    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # use a generic view
    request.function = 'Alterar registro financeiro'

    # Cria e processa o formulário de alteração
    form = SQLFORM(db.registro_financeiro, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        redirect(URL('index', args=pagina))
    elif form.errors:
        response.flash = 'Formulário não aceito'

    # Retorna o formulário para a visualização
    return dict(form=form)
