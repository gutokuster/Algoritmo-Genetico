#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@date: Jan/21
@author: @gkuster
@v_1.0

"""
# Individuos: Representam as possibilidades/soluções e formam populações. 
# Cromossomos: Rrepresentam a solução

from random import random

class Produto:
    def __init__(self,cod,nome,espaco,valor):
        self.cod=cod
        self.nome=nome
        self.espaco=espaco
        self.valor=valor
        
        
class Individuo():
    def __init__(self,espacos,valores,limite_espacos,geracao=0):
        self.espacos = espacos
        # R$
        self.valores = valores                
        # Espaço máximo para o armazenamento dos itens, em M³
        self.limite_espacos = limite_espacos  
        # Nota que cada indivíudo irá receber. Comparativo com outros indivíduos
        self.nota_avaliacao = 0               
        self.geracao = geracao
        # Recebe valor 0 (não carrega) ou 1 (carrega)
        self.cromossomo = []
        
        for i in range(len(espacos)):
            # 50% de probabilidade para receber 0 ou 1
            if random() < 0.5: 
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")        
            
        
if __name__ == '__main__':
    # p1 = Produto('Iphone 6',0.0000899,2199.12)
    lista_produtos = []
    lista_produtos.append(Produto(1,"Geladeira Dako", 0.751, 999.90))
    lista_produtos.append(Produto(2,"Iphone 6", 0.0000899, 2911.12))
    lista_produtos.append(Produto(3,"TV 55' ", 0.400, 4346.99))
    lista_produtos.append(Produto(4,"TV 50' ", 0.290, 3999.90))
    lista_produtos.append(Produto(5,"TV 42' ", 0.200, 2999.00))
    lista_produtos.append(Produto(6,"Notebook Dell", 0.00350, 2499.90))
    lista_produtos.append(Produto(7,"Ventilador Panasonic", 0.496, 199.90))
    lista_produtos.append(Produto(8,"Microondas Electrolux", 0.0424, 308.66))
    lista_produtos.append(Produto(9,"Microondas LG", 0.0544, 429.90))
    lista_produtos.append(Produto(10,"Microondas Panasonic", 0.0319, 299.29))
    lista_produtos.append(Produto(11,"Geladeira Brastemp", 0.635, 849.00))
    lista_produtos.append(Produto(12,"Geladeira Consul", 0.870, 1199.89))
    lista_produtos.append(Produto(13,"Notebook Lenovo", 0.498, 1999.90))
    lista_produtos.append(Produto(14,"Notebook Asus", 0.527, 3999.00))
    #for produto in lista_produtos:
    #    print(produto.cod)
    
    espacos = []
    valores = []
    nomes   = []
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
    limite = 3
    
    individuo1 = Individuo(espacos, valores, limite)
    print("Espaços = %s" %  str(individuo1.espacos))
    print("Valores = %s" %  str(individuo1.valores))
    print("Cromossomo = %s" %  str(individuo1.cromossomo))
    
    print("\nCarga:")
    for i in range(len(lista_produtos)):
        if individuo1.cromossomo[i] == '1':
            print("Cód: %s  | Nome: %s  (R$ %s) "  % (lista_produtos[i].cod, lista_produtos[i].nome, lista_produtos[i].valor))
    
