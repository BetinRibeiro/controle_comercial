# -*- coding: utf-8 -*-
# tente algo como
def dre():
    response.view = 'mensagem.html'  # use a generic view
    definicao = 'A Demonstração do Resultado do Exercício (DRE) é um relatório financeiro que apresenta o desempenho financeiro de uma empresa durante um determinado período, geralmente um ano fiscal. Também conhecida como Demonstração de Resultados ou Demonstrativo de Lucros e Perdas, a DRE é uma das principais demonstrações financeiras utilizadas para avaliar a saúde financeira e a eficiência operacional de uma empresa.'
    return dict(definicao=definicao)



def bp():
    response.view = 'mensagem.html'  # use a generic view
    definicao = 'O Balanço Patrimonial é um relatório contábil que apresenta a posição financeira de uma empresa em um determinado momento, mostrando o equilíbrio entre seus ativos, passivos e patrimônio líquido. Essa demonstração financeira é fundamental para avaliar a saúde financeira, a solvência e a estrutura de financiamento de uma organização.'
    return dict(definicao=definicao)
