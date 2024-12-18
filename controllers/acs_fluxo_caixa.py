# -*- coding: utf-8 -*-
from datetime import date, timedelta

@auth.requires_login()
def index():
    if len(request.args) == 0:
        posicao = 0
    else:
        try:
            posicao = int(request.args[0])
        except ValueError:
            redirect(URL(0))
    hj = date.today()
    data_inicial = hj + timedelta(days=posicao - 1)
    data_final = hj + timedelta(days=posicao + 1)

    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)


    operacoes_empresa = db(db.operacao.empresa == empresa.id)._select(db.operacao.id)

    rows = db((db.registro_financeiro.operacao.belongs(operacoes_empresa)) &
                   (db.registro_financeiro.data_vencimento > data_inicial) &
                   (db.registro_financeiro.data_vencimento < data_final)).select(
                       orderby=db.registro_financeiro.liquidado | ~db.registro_financeiro.tipo,
                       join=db.operacao.on(db.operacao.id == db.registro_financeiro.operacao))

    hoje = hj + timedelta(days=posicao)
    rows_atrasado = db((db.registro_financeiro.operacao.belongs(operacoes_empresa)) &
                             (db.registro_financeiro.data_vencimento < hoje) &
                             (db.registro_financeiro.liquidado == False)).select()

    liberado = len(rows) > 0

    return locals()
