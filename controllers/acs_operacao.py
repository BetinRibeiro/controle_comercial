# -*- coding: utf-8 -*-
# tente algo como

@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    if not usuario.ativo:
        redirect(URL('default', 'index'))

    paginacao = empresa.paginacao
    if len(request.args) == 0:
        pagina = 1
    else:
        try:
            pagina = int(request.args[0])
        except ValueError:
            redirect(URL(args=[1]))

    if pagina <= 0:
        pagina = 1
    total = db((db.operacao.empresa == empresa.id)).count()
    paginas = total // paginacao
    if total % paginacao:
        paginas += 1
    if total == 0:
        paginas = 1
    if pagina > paginas:
        redirect(URL(args=[paginas]))

    limites = (paginacao * (pagina - 1), (paginacao * pagina))

    registros = db((db.operacao.empresa == empresa.id)).select(
        limitby=limites, orderby=~db.operacao.id | db.operacao.codigo)
    consul = request.args(1)
    if consul:
        registros = db((db.operacao.empresa == empresa.id) & (
            (db.operacao.codigo.contains(consul)))).select(
            limitby=limites, orderby=db.operacao.codigo)

    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa)


@auth.requires_login()
def cadastrar():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    response.view = 'generic.html'
    request.function = 'Cadastro de operação'

    db.operacao.empresa.default = usuario.empresa
    form = SQLFORM(db.operacao).process()

    if form.accepted:
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Formulário não aceito'

    return dict(form=form)


@auth.requires_login()
def alterar():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    operacao = db.operacao(request.args(0, cast=int))

    if len(request.args) == 1:
        pagina = 1
    else:
        pagina = int(request.args[1])

    if operacao.empresa != usuario.empresa:
        redirect(URL('index'))

    response.view = 'generic.html'
    request.function = 'Alterar operação'

    form = SQLFORM(db.operacao, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        redirect(URL('index', args=pagina))
    elif form.errors:
        response.flash = 'Formulário não aceito'

    return dict(form=form)
