# -*- coding: utf-8 -*-
def atualizar_precos_custo_produto(id_produto):
    produto = db.produto(id_produto)

    # Busca a última operação relacionada a este produto
    ultima_operacao = db((db.produto_operacao.produto == id_produto) &
                         (db.produto_operacao.finalizado == True)).select(
                         orderby=~db.produto_operacao.id, limitby=(0, 1)).first()

    if ultima_operacao:
        novo_preco_unitario = ultima_operacao.preco_unitario
        novo_custo_unitario = ultima_operacao.custo_unitario

        # Atualiza o preço e custo do produto
        db(db.produto.id == id_produto).update(preco_unitario=novo_preco_unitario,
                                               custo_unitario=novo_custo_unitario)

        return novo_preco_unitario, novo_custo_unitario
    else:
        return None, None

def atualizar_estoque_produto(id_produto):
    produto = db.produto(id_produto)

    # Calcula o estoque atual a partir das operações de entrada e saída
    estoque_atual = produto.quantidade_estoque
    operacoes_entrada = db((db.produto_operacao.produto == id_produto) &
                           (db.produto_operacao.tipo_movimentacao == 'entrada')).select(
                           db.produto_operacao.quantidade.sum()).first()[db.produto_operacao.quantidade.sum()]

    operacoes_saida = db((db.produto_operacao.produto == id_produto) &
                         (db.produto_operacao.tipo_movimentacao == 'saida')).select(
                         db.produto_operacao.quantidade.sum()).first()[db.produto_operacao.quantidade.sum()]
    estoque_atual=0
    if operacoes_entrada:
        estoque_atual += float(operacoes_entrada)
    if operacoes_saida:
        estoque_atual -= float(operacoes_saida)

    # Atualiza o estoque do produto
    db(db.produto.id == id_produto).update(quantidade_estoque=estoque_atual)
    atualizar_precos_custo_produto(id_produto)
    return estoque_atual
