# -*- coding: utf-8 -*-

def curva_abc():
    response.view = 'mensagem.html'  # use a generic view
    definicao = 'A Curva ABC, também conhecida como Análise ABC, é uma técnica de classificação e priorização de elementos com base em sua importância relativa. Ela é amplamente utilizada em várias áreas, como gestão de estoque, finanças, marketing e gerenciamento de projetos, para focar recursos onde eles terão o maior impacto.'
    return dict(definicao=definicao)



def despesas():
    response.view = 'mensagem.html'  # use a generic view
    definicao = 'Uma listagem de despesas é uma relação detalhada dos gastos incorridos por uma empresa ou indivíduo durante um determinado período de tempo. Essa listagem é uma parte importante da gestão financeira, pois permite entender onde o dinheiro está sendo gasto e identificar áreas de redução de custos ou otimização. '
    return dict(definicao=definicao)

def estoque_minimo():
    response.view = 'mensagem.html'  # use a generic view
    definicao = 'O indicador de estoque mínimo é uma métrica usada para determinar o nível mínimo de produtos ou materiais que uma empresa precisa manter em estoque para atender às demandas sem interrupções. Esse indicador é importante para evitar situações de falta de produtos, que podem resultar em atrasos nas entregas ou perda de vendas.'
    return dict(definicao=definicao)

def direcionamento():
    response.view = 'mensagem.html'  # use a generic view
    definicao = 'Se você deseja consultar um produto com base na sua observação para saber para que ele é indicado, é importante que o campo de observação esteja registrado na sua base de dados. Assumindo que você está usando um banco de dados, você pode realizar uma consulta SQL para buscar produtos com uma determinada observação. '
    return dict(definicao=definicao)
