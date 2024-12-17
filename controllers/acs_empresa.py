# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
#     db((db.registro_financeiro.descricao.contains('vista')) & (db.registro_financeiro.liquidado == False)).update(liquidado=True)
    """
    Função: index
    Descrição: Página inicial após o login, gerenciando redirecionamentos com base nas informações do usuário.
    Requisitos: O usuário deve estar autenticado para acessar esta função.
    """

    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    # Obtém informações do usuário a partir do banco de dados "usuario_empresa".
    # Isso filtra o usuário pelo ID de autenticação atual (auth.user.id).

    if not usuario:
        redirect(URL('acs_empresa', 'cadastrar'))
    # Se não houver informações de usuário, redireciona para a página de cadastro da empresa.
    # Isso provavelmente significa que o usuário está acessando pela primeira vez.

    if usuario.tipo == "#":
        redirect(URL('acs_algum', 'index'))
    # Se o tipo de usuário for "#", redireciona para a página do representante da empresa.
    # Isso pode estar relacionado a algum tipo específico de privilégio ou função.

    if usuario.ativo == False:
        redirect(URL('default', 'index'))
    # Se o usuário não estiver ativo, redireciona para a página inicial.
    # Isso pode significar que o usuário foi desativado ou precisa ativar sua conta.

    empresa = db.empresa(usuario.empresa)
    # Obtém informações sobre a empresa a partir do banco de dados "empresa".
    # Isso usa o ID da empresa associado ao usuário.

    liberado = False
    if len(request.args) == 1:
        liberado = True
    # Verifica se há um argumento na solicitação.
    # Se houver exatamente um argumento, define a variável "liberado" como True.

    return locals()
    # Retorna um dicionário contendo as variáveis locais da função.
    # Isso é usado para passar as variáveis para o template da página.

@auth.requires_login()
def cadastrar():
    """
    Função: cadastrar
    Descrição: Cadastra uma nova empresa associada ao usuário logado e redireciona para a página inicial.
    Requisitos: O usuário deve estar autenticado para acessar esta função.
    """

    # Insere uma nova entrada na tabela "empresa" com base nas informações do usuário logado.
    # O nome da empresa é definido como o primeiro nome do usuário seguido de " Empresarial".
    empresa = db.empresa.insert(nome=auth.user.first_name + " Empresarial")

    # Insere uma nova entrada na tabela "usuario_empresa" associando a empresa ao usuário logado.
    # Também define o nome do usuário associado à empresa.
    db.usuario_empresa.insert(empresa=empresa, usuario=auth.user.id, nome=empresa.nome)

    # Redireciona o usuário para a página inicial após o cadastro da empresa.
    return redirect(URL('index'))

@auth.requires_login()
def alterar():
    """
    Função: alterar
    Descrição: Permite ao usuário autenticado alterar informações da empresa associada.
    Requisitos: O usuário deve estar autenticado para acessar esta função.
    """

    # Define a view como 'generic.html' para utilizar um template genérico.
    response.view = 'generic.html'

    # Redefine o nome da função para "Alterar".
    request.function = 'Alterar'

    # Obtém informações do usuário a partir do banco de dados "usuario_empresa".
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    if auth.user.id==1:
        db.empresa.qunat_user.label = "Usuarios ==>"
        db.empresa.qunat_user.writable = True
        db.empresa.qunat_user.readable = True
        db.empresa.paginacao.label = "Paginação ==>"
        db.empresa.paginacao.writable = True
        db.empresa.paginacao.readable = True
    # Cria um formulário para editar as informações da empresa associada ao usuário.
    # O formulário é preenchido com os dados da empresa obtidos do banco de dados.
    # A opção "deletable=False" impede a exclusão acidental da empresa.
    form = SQLFORM(db.empresa, usuario.empresa, deletable=False)

    # Processa o formulário quando for enviado.
    if form.process().accepted:
        redirect(URL('index'))
        # Redireciona para a página inicial após o processamento bem-sucedido do formulário.

    # Exibe uma mensagem de erro se houver problemas no formulário.
    elif form.errors:
        response.flash = 'Erros no formulário!'

    # Retorna um dicionário contendo o formulário para ser usado no template da página.
    return dict(form=form)

@auth.requires_login()
def alterar_usuario():
    """
    Função: alterar_usuario
    Descrição: Permite a alteração de informações de um usuário associado à empresa.
    Requisitos: O usuário deve estar autenticado para acessar esta função.
    """

    # Define a view como 'generic.html' para utilizar um template genérico.
    response.view = 'generic.html'

    # Obtém informações do usuário a partir do banco de dados "usuario_empresa".
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)

    # Verifica se o usuário logado possui permissão para acessar esta função.
    if auth.user.id != 1:
        redirect(URL('index'))
        # Redireciona para a página inicial se o usuário não tiver permissão.

    # Redefine o nome da função para "Alterar nome da Empresa".
    request.function = 'Alterar nome da Empresa'

    # Habilita a edição do campo "empresa" na tabela "usuario_empresa".
    db.usuario_empresa.empresa.writable = True
    db.usuario_empresa.empresa.readable = True

    # Cria um formulário para editar as informações do usuário.
    # O formulário é preenchido com os dados do usuário obtidos do banco de dados.
    # A opção "deletable=False" impede a exclusão acidental do usuário.
    form = SQLFORM(db.usuario_empresa, usuario.id, deletable=False)

    # Processa o formulário quando for enviado.
    if form.process().accepted:
        redirect(URL('index'))
        # Redireciona para a página inicial após o processamento bem-sucedido do formulário.

    # Exibe uma mensagem de erro se houver problemas no formulário.
    elif form.errors:
        response.flash = 'Erros no formulário!'

    # Retorna um dicionário contendo o formulário para ser usado no template da página.
    return dict(form=form)
