# -*- coding: utf-8 -*-
from datetime import date
def dinheiro(numero):
    try:
        numero = float(numero)
        retorno = "R$ {:,.2f}".format(round(numero,2)).replace(",","#").replace(".",",").replace("#",".")
    except:
        retorno = "ERRO!"
    return retorno


def gerar_codigo(ano_mes_dia, id_usuario, ultimo_id_operacao):
    # Formata a data no formato YYYYMMDD
    data_formatada = ano_mes_dia.strftime('%Y%m%d')
    
    # Converte o id do cliente para string e ajusta para ter 2 dígitos
    id_usuario_str = str(id_usuario).zfill(2)
    
    # Converte o último id da operação para string e ajusta para ter 5 dígitos
    ultimo_id_operacao_str = str(ultimo_id_operacao).zfill(8)
    
    # Combina as partes para formar a codificação completa
    codigo_final = f"{data_formatada}{id_usuario_str}{ultimo_id_operacao_str}"
    
    return codigo_final


def salvar_operacao(id_operacao):
    operacao = db.operacao(id_operacao)

    if operacao.tipo == 'venda':
        tipo_registro = 'recebimento'
        valor_registro = operacao.valor_total
    elif operacao.tipo == 'compra':
        tipo_registro = 'pagamento'
        valor_registro = operacao.custo_total
    else:
        return  # Operação não é nem venda nem compra

    pessoa = db.pessoa(operacao.pessoa)
    if pessoa:
        data_vencimento =  date.fromordinal(operacao.created_on.toordinal()+pessoa.dias_prazo)
        descricao = f'Op - {auth.user.id+10} | {tipo_registro.title()} - {operacao.codigo} - {pessoa.nome} - dia {operacao.created_on.strftime("%d/%m/%Y")} - Valor Total - {dinheiro(valor_registro)}'
        finalizado=False
    else:
        data_vencimento=operacao.created_on
#     data_vencimento = operacao.created_on + timedelta(days=pessoa.dias_prazo) if pessoa else None
        descricao = f'Op - {auth.user.id+10} | {tipo_registro.title()} - {operacao.codigo} - à Vista - dia {operacao.created_on.strftime("%d/%m/%Y")} - Valor Total - {dinheiro(valor_registro)}'
        finalizado=True
    registro_financeiro = db(
        (db.registro_financeiro.operacao == id_operacao) &
        (db.registro_financeiro.tipo == tipo_registro)
    ).select().first()

    if registro_financeiro:
        registro_financeiro.update_record(
            data_vencimento=data_vencimento,
            descricao=descricao,
            valor=valor_registro,
            liquidado=finalizado
        )
    else:
        db.registro_financeiro.insert(
            operacao=id_operacao,
            data_vencimento=data_vencimento,
            descricao=descricao,
            tipo=tipo_registro,
            valor=valor_registro,
            liquidado=finalizado
        )
    return True
