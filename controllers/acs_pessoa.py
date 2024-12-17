# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)
    tipo=(request.args[0])
    if not usuario.ativo:
        redirect(URL('default', 'index'))

    paginacao = empresa.paginacao
    if len(request.args) == 1:
        pagina = 1
    else:
        try:
            pagina = int(request.args[1])
        except ValueError:
            redirect(URL(args=[tipo,1]))

    if pagina <= 0:
        pagina = 1
    total = db((db.pessoa.empresa == empresa.id)&(db.pessoa.tipo == tipo)).count()
    paginas = total // paginacao
    if total % paginacao:
        paginas += 1
    if total == 0:
        paginas = 1
    if pagina > paginas:
        redirect(URL(args=[tipo,paginas]))

    limites = (paginacao * (pagina - 1), (paginacao * pagina))

    registros = db((db.pessoa.empresa == empresa.id)&(db.pessoa.tipo == tipo)).select(
        limitby=limites, orderby=~db.pessoa.id | db.pessoa.nome)
    consul = request.args(2)
    if consul:
        registros = db((db.pessoa.empresa == empresa.id) & (db.pessoa.tipo == tipo) & (
            (db.pessoa.nome.contains(consul)))).select(
            limitby=limites, orderby=db.pessoa.nome)

    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa,tipo=tipo)
@auth.requires_login()
def cadastrar():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)
    tipo = request.args(0)

    response.view = 'generic.html'
    request.function = 'Cadastro de pessoa'

    db.pessoa.tipo.default = tipo
    db.pessoa.empresa.default = usuario.empresa
    form = SQLFORM(db.pessoa).process()

    if form.accepted:
        redirect(URL('index',args=tipo))
    elif form.errors:
        response.flash = 'Formulário não aceito'

    return dict(form=form)
@auth.requires_login()
def alterar():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    pessoa = db.pessoa(request.args(0, cast=int))
    tipo=pessoa.tipo
    if len(request.args) == 1:
        pagina = 1
    else:
        pagina = int(request.args[1])

    if pessoa.empresa != usuario.empresa:
        redirect(URL('index',args=tipo))

    response.view = 'generic.html'
    request.function = 'Alterar pessoa'

    form = SQLFORM(db.pessoa, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        redirect(URL('index', args=[tipo,pagina]))
    elif form.errors:
        response.flash = 'Formulário não aceito'

    return dict(form=form)
