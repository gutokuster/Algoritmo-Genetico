#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @date: Jan/21   @author: @gkuster   @v_1.0

###############################################################################
# Variáveis
# limite = 3
# tamanho_populacao = 50
# taxa_mutacao = 0.01
# numero_geracoes = 500
##############################################################################
# Individuos: Representam as possibilidades/soluções e formam populações. 
#
# Cromossomos: Representam a solução
#
# Função Fitness (Avaliação): Medida de qualidade. Verifica se uma solução é 
#                              aceitável e se pode ser utilizada na evolução.
#
# Crossover (Reprodução): Gera filhos mais aptos a partir de dois cromossomos, 
#                          tendendo a evoluir a população a cada nova geração.
#
# Mutação: Muda aleatóriamente os genes de um indivíduo. Ocorre com menos  
#                                                  frequência que o crossover.
#
# Indivíduos com melhor avaliação serão selecionados e suas características 
# devem predominar na nova população. As melhores avaliações devem ser 
# priorizadas sem desprezar as avalições baixas, caso contrário, novas
# populações tendem a ser semelhantes e faltará diversidade.
#
##############################################################################
# TODO
# * Coletar dados de BD - MySql e MongoDB
# * Validar se pais são diferentes
# * Gerar lista com Top 10 dos resultados e apresenta em gráfico
##############################################################################

import matplotlib.pyplot as plt
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
        self.valores = valores                
        self.limite_espacos = limite_espacos  
        self.nota_avaliacao = 0               
        self.geracao = geracao
        self.cromossomo = []
        self.espaco_utilizado = 0
        
        for i in range(len(espacos)):
            # 50% de probabilidade para receber 0 ou 1
            if random() < 0.5: 
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")        
           
    def avaliacao(self):
        nota = 0
        soma_espacos = 0
        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == '1':
                nota += self.valores[i]
                soma_espacos += self.espacos[i]
            if soma_espacos > self.limite_espacos:
                nota = 1
            self.nota_avaliacao = nota
            self.espaco_utilizado = soma_espacos
            
    def crossover(self,outro_individuo):
        corte = round(random() * len(self.cromossomo))
        
        self.outro_individuo = outro_individuo 
        
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        
        filhos = [Individuo(self.espacos, self.valores, self.limite_espacos, 
                            self.geracao + 1),
                  Individuo(self.espacos, self.valores, self.limite_espacos, 
                            self.geracao + 1)]
        
        filhos[0].cromossomo = filho1 
        filhos[1].cromossomo = filho2
        return filhos
    
    def mutacao(self, taxa_mutacao):
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        return self
    
class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = []
        
    def inicializa_populacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(espacos, valores, limite_espacos))
        self.melhor_solucao = self.populacao[0]
        
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                            key = lambda populacao: populacao.nota_avaliacao,
                            reverse = True)
    
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
            
    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
        return soma
    
    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai 
       
    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("G:%s -> Valor: %s Espaço: %s Cromossomo: %s" % 
                                                  (self.populacao[0].geracao,
                                                   melhor.nota_avaliacao,
                                                   melhor.espaco_utilizado,
                                                   melhor.cromossomo))
        
    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espacos):
        self.inicializa_populacao(espacos, valores, limite_espacos)
        for individuo in self.populacao:
            individuo.avaliacao()

            self.ordena_populacao()
            self.melhor_solucao = self.populacao[0]
            self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
            self.visualiza_geracao()
            
            for geracao in range(numero_geracoes):
                soma_avaliacao = self.soma_avaliacoes()
                nova_populacao = []
                
                for individuos_gerados in range(0,self.tamanho_populacao,2):
                    pai1 = self.seleciona_pai(soma_avaliacao)
                    pai2 = self.seleciona_pai(soma_avaliacao)
                
                    filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                    
                    nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                    nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
                
                self.populacao = list(nova_populacao)
                
                for individuo in self.populacao:
                    individuo.avaliacao()
            
                self.ordena_populacao()
            
                self.visualiza_geracao()
            
                melhor = self.populacao[0]
                self.lista_solucoes.append(melhor.nota_avaliacao)
                self.melhor_individuo(melhor)
           
            print("\nMelhor solução -> G:%s Valor: %s Espaço: %s Cromossomo: %s" % 
                  (self.melhor_solucao.geracao,
                   self.melhor_solucao.nota_avaliacao,
                   self.melhor_solucao.espaco_utilizado,
                   self.melhor_solucao.cromossomo))
            
            return self.melhor_solucao.cromossomo
            
                    
if __name__ == '__main__':
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
    
    espacos = []
    valores = []
    nomes   = []
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
   
    limite = 3
    tamanho_populacao = 50
    taxa_mutacao = 0.01
    numero_geracoes = 500
    
    ag = AlgoritmoGenetico(tamanho_populacao)
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite)
    for i in range(len(lista_produtos)):
        if resultado[i] == '1':
            print("Nome: %s R$ %s " % (lista_produtos[i].nome,
                                       lista_produtos[i].valor))
            
    plt.plot(ag.lista_solucoes)
    plt.title("Evolução dos valores Obtidos")
    plt.show()
