#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @date: Jan/21   @author: @gkuster

import random
import numpy
import pymysql
from deap import base
from deap import creator
from deap import algorithms
from deap import tools
import matplotlib.pyplot as plt

class Produto:
    def __init__(self,cod,nome,espaco,valor):
        self.cod=cod
        self.nome=nome
        self.espaco=espaco
        self.valor=valor

lista_produtos = []
conexao = pymysql.connect(host='localhost', user='root', password='root', 
                          db='produtos')
cursor = conexao.cursor()
cursor.execute('select idproduto, nome, espaco, valor, quantidade from produtos')
for produto in cursor:
    for i in range(produto[4]):
        lista_produtos.append(Produto(produto[0], produto[1], produto[2], produto[3]))
print(lista_produtos)
cursor.close()
conexao.close()  
    
espacos = []
valores = []
nomes   = []
for produto in lista_produtos:
    espacos.append(produto.espaco)
    valores.append(produto.valor)
    nomes.append(produto.nome)

limite = 5

toolbox = base.Toolbox()
creator.create("FitnessMax", base.Fitness, weights=(1.0, ))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_bool, n=len(espacos))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def avaliacao(individual):
    nota = 0
    soma_espacos = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            nota += valores[i]
            soma_espacos += espacos[i]
    if soma_espacos > limite:
        nota = 1
    return nota / 100000,
    
toolbox.register("evaluate", avaliacao)
toolbox.register("mate", tools.cxOnePoint)      # Tipo do crossover
toolbox.register("mutate", tools.mutFlipBit, indpb = 0.01) # Tipo/Taxa de mutação
toolbox.register("select", tools.selRoulette)   # Função de seleção dos indivíduos para  mutação

if __name__ == "__main__":
    
       
    # random.seed(1)
    populacao = toolbox.population(n = 20)
    probabilidade_crossover = 1.0
    probabilidade_mutacao = 0.01
    numero_geracoes = 100
    
    estatisticas = tools.Statistics(key=lambda individuo: individuo.fitness.values)
    estatisticas.register("max", numpy.max)
    estatisticas.register("min", numpy.min)
    estatisticas.register("med", numpy.mean)
    estatisticas.register("std", numpy.std) # Desvio padrão

    populacao, info = algorithms.eaSimple(populacao, toolbox, probabilidade_crossover, 
                                          probabilidade_mutacao, numero_geracoes, estatisticas)      
    
    mostra_melhores = 1
    melhores = tools.selBest(populacao, mostra_melhores)
    for individuo in melhores:
        #print(individuo)
        #print(individuo.fitness)
        soma = 0
        espaco = 0
        for i in range(len(lista_produtos)):
            if individuo[i] == 1:
                soma += valores[i]
                espaco += espacos[i]
                print("Nome: %s R$ %s Espaço: %s" % (lista_produtos[i].nome,
                                          lista_produtos[i].valor,
                                          lista_produtos[i].espaco))
        print("Melhor solução: R$ %s Espaço: %s" % (soma, espaco))
        
    valores_grafico = info.select("max")
    plt.plot(valores_grafico)
    plt.title("Evolução dos valores Obtidos")
    plt.show()