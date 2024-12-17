# -*- coding: utf-8 -*-

db.define_table('produto',
    Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
    Field('descricao', 'string', label='Descrição', requires=IS_NOT_EMPTY(), default="Produto 0"),
    Field('custo_unitario', 'double', label='Custo Unitário', requires=IS_FLOAT_IN_RANGE(0, None), default=0),
    Field('preco_unitario', 'double', label='Preço Unitário', requires=IS_FLOAT_IN_RANGE(0, None), default=0),
    Field('quantidade_estoque', 'double', writable=False, label='Quantidade em Estoque', default=0),
    Field('quantidade_minima', 'double', label='Quantidade Mínima', requires=IS_FLOAT_IN_RANGE(0, None), default=0),
    Field('data_atualizacao', 'date', writable=False, readable=True, default=request.now, label='Data de Atualização'),
    Field('codigo_barras', 'string', label='Código de Barras', requires=[IS_NOT_EMPTY()]),
    Field('ativo', 'boolean', writable=True, readable=True, default=True),
    auth.signature,
    format='%(descricao)s')

db.produto.id.writable = False
db.produto.id.readable = False

db.define_table('pessoa',
    Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
    Field('nome', 'string', label='Nome', requires=IS_NOT_EMPTY(), default=""),
    Field('dias_prazo', 'integer', label='Prazo', default=30),
    Field('tipo', 'string', label='Tipo', writable=False, readable=False, requires=IS_NOT_EMPTY(), default=""),
    Field('limite_credito', 'double', writable=True, readable=True, label='Limite Crédito', requires=IS_FLOAT_IN_RANGE(0, None), default=0),
    Field('valor_total', 'double', writable=False, readable=False, label='Valor Total', requires=IS_FLOAT_IN_RANGE(0, None), default=0),
    Field('valor_quitado', 'double', writable=False, readable=False, label='Valor Quitado', requires=IS_FLOAT_IN_RANGE(0, None), default=0),
    Field('valor_aguardando', 'double', writable=False, readable=False, label='Valor Aguardando', requires=IS_FLOAT_IN_RANGE(0, None), default=0),
    Field('valor_pendente', 'double', writable=False, readable=False, label='Valor Pendente', requires=IS_FLOAT_IN_RANGE(0, None), default=0),
    Field('data_atualizacao', 'date', writable=False, readable=False, default=request.now, label='Data de Atualização'),
    Field('ativo', 'boolean', writable=True, readable=True, default=True),
    auth.signature,
    format='%(nome)s')

db.pessoa.id.writable = False
db.pessoa.id.readable = False

db.define_table('operacao',
    Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
    Field('pessoa','reference pessoa', writable=False, readable=False, label='Cliente/Fornecedor'),
    Field('codigo', 'string', label='Código', writable=False, readable=True, requires=IS_NOT_EMPTY(), default=""),
    Field('tipo', 'string', label='Tipo', writable=False, readable=False, requires=IS_NOT_EMPTY(), default=""),
    Field('valor_total', 'double', writable=False, readable=True, label='Custo Unitário', requires=IS_FLOAT_IN_RANGE(0, None), default=0),
    Field('custo_total', 'double', writable=False, readable=True, label='Preço Unitário', requires=IS_FLOAT_IN_RANGE(0, None), default=0),
    Field('ativo', 'boolean', writable=True, readable=True, default=False),
    auth.signature,
    format='%(codigo)s')

db.operacao.id.writable = False
db.operacao.id.readable = False

db.define_table('produto_operacao',
    Field('produto', 'reference produto', writable=False, readable=False, label='Produto'),
    Field('operacao', 'reference operacao', writable=False, readable=False, label='Operacao'),
    Field('tipo_movimentacao', 'string', writable=False, readable=False,default="saida", requires=IS_IN_SET(['entrada', 'saida']), label='Tipo'),
    Field('quantidade', 'decimal(10, 2)', label='Quantidade'),
    Field('custo_unitario', 'double', writable=False, readable=False, label='Custo Unitário', requires=IS_FLOAT_IN_RANGE(0, None)),
    Field('preco_unitario', 'double', writable=False, readable=True, label='Preço', requires=IS_FLOAT_IN_RANGE(0, None)),
    Field('data_operacao', 'date', writable=False, readable=False, default=request.now, label='Data'),
    Field('finalizado', 'boolean', writable=False, readable=False, default=False),
    auth.signature,
    format='%(tipo_movimentacao)s - Produto: %(produto.nome)s - Operação: %(operacao.descricao)s')

db.produto_operacao.id.writable = False
db.produto_operacao.id.readable = False

db.define_table('registro_financeiro',
    Field('operacao', 'reference operacao', writable=False, readable=False, label='Operacao'),
    Field('data_vencimento', 'date', writable=False, readable=False, default=request.now, label='Vencimento'),
    Field('descricao', 'string', label='Descrição', requires=IS_NOT_EMPTY(), default=""),
    Field('tipo', 'string', writable=False, readable=False,default="recebimento", requires=IS_IN_SET(['recebimento', 'pagamento']), label='Tipo'),
    Field('valor', 'double', writable=False, readable=False, label='Valor', requires=IS_FLOAT_IN_RANGE(0, None)),
    Field('finalizado', 'boolean', writable=False, readable=False, default=False),
    Field('liquidado', 'boolean', writable=False, readable=False, default=False),
    auth.signature,
    format='%(descricao)s')

db.registro_financeiro.id.writable = False
db.registro_financeiro.id.readable = False

db.define_table('patrimonio',
    Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
    Field('descricao', 'string', label='Descrição', writable=True, readable=True, requires=IS_NOT_EMPTY(), default=""),
    Field('tipo', 'string', label='Tipo', writable=True, readable=True, requires=IS_NOT_EMPTY(), default="Transporte"),
    Field('valor', 'double', writable=True, readable=True, label='Valor', requires=IS_FLOAT_IN_RANGE(0, None), default=0),
    Field('ativo', 'boolean', writable=True, readable=True, default=False),
    auth.signature,
    format='%(descricao)s')

db.patrimonio.id.writable = False
db.patrimonio.id.readable = False
db.patrimonio.tipo.requires=IS_IN_SET(['Transporte','Móveis', 'Imóveis', 'Ferramentas', 'Outro'])
