#!/usr/bin/env python
# coding: utf-8

# # Equipe
# ### Nome: Alessandro Souza Silva       Mat: 399941
# ### Nome: Diego Gaspar da Cruz         Mat: 398326

# A equipe escolheu representar as alocações como uma string de bits que em python é representado como uma lista de bits

# In[1]:


from heapq import * # Estrutura auxiliar na implementação da técnica 'Busca pelo Melhor Primeiro'
from random import randint # Método para gerar valor aleatório
from random import choice # Método para selecionar item aleatório
from random import choices # Método para selecionar item aleatório cde acordo com pesos
from random import uniform # Método para selecionar valor aleatório
from math import exp

# Método para gerar uma lista binária aleatória
aleatorio = lambda x : [randint(0,1) for _ in range(0,x)]


# # Estado de Busca

# In[2]:


# Representação de um estado

class Estado( object ):

    #Construtor
    def __init__( self, k = 10, n = 21, string = [] ):
        self.k = k
        self.n = n
        # Se a lista string / lista binária não é passada como parâmetro, ela é gerada aleatoriamente
        if len(string) == k*n:
            self.string = string
        else:
            self.string = aleatorio(k*n)
    
    def __lt__(self,estado):
        return True
    
    def tam( self ):
        return self.k*self.n


# In[3]:


#Função extra para uma visualização mais agradável das alocações / lista de bits
def Visualizar_Estado( e ):

    inicio = 0
    final = e.n
    for k in range(e.k):
        l = []
        for n in e.string[inicio:final]:
            l.append(n)
        inicio = final
        final = final + e.n
        print("Enfer ",k,l)


# # Restrições do Problema

# In[4]:


# RESTRIÇÃO 1 : 'Deve haver ao menos 1 enfermeiro e no máximo 3 enfermeiros em cada turno'. 

# ENTRADA: Estado e
# SAÍDA:   Avaliação do estado e com base na restrição 1
def g_restricao01( e ): 
    
    #Iniciando uma lista zerada para guardar a quantidade de enfermeiros em cada turno
    s = [ 0 for _ in range(e.n) ]
    
    #Preenchendo a lista s.
    for n in range( e.n ):
        i = n
        for k in range( e.k ):
            s[n] = s[n] + e.string[i]
            i = i + e.n
    
    #Variável para guardar a avaliação do estado
    aval = 0
    
    #Para cada elemento s1 em s: se s1 tem valor entre 1 e 3, então não ocorre mudanças na avaliação
                         #       se s1 for igual a zero, então a avaliação é incrementada em 1
                         #       se s1 for maior que 3, então a avaliação é incrementada em (s1-3)
    for s1 in s:
        if 1 <= s1 <= 3:
            continue
        elif s1 == 0:
            aval = aval + 1
        else:
            aval = aval + s1-3
            
    return aval


# In[5]:


# RESTRIÇÃO 2 : 'Cada enfermeiro deve ser alocado em 5 turnos por semana'. 

# ENTRADA: Estado e
# SAÍDA:   Avaliação do estado e com base na restrição 2
def g_restricao02( e ):
    
    #Iniciando uma lista zerada para guardar a quantidade de turnos alocados para cada enfermeiro
    s = [ 0 for _ in range(e.k) ]
    
    #Preenchendo a lista s
    inicio = 0
    final = e.n
    for k in range(e.k):
        for n in e.string[inicio:final]:
            s[k] = s[k] + n
        inicio = final
        final = final + e.n
        
    #Variável para guardar a avaliação do estado
    aval = 0
    
    #Para cada elemento s1 em s, a avaliação é incrementada em abs(s1-5)
    for s1 in s:
        aval = aval + abs(s1-5)
        
    return aval


# In[6]:


# RESTRIÇÃO 3 : 'Nenhum enfermeiro pode trabalhar mais que 3 turnos seguidos sem folga'. 

# ENTRADA: Estado e
# SAÍDA:   Avaliação do estado e com base na restrição 3
def g_restricao03( e ):
    
    # Iniciando uma lista zerada para guardar a quantidade de vezes que um enfermeiro 
    # trabalhou pelo menos quatro turnos seguidos 
    # ( Ou seja, se um enfermeiro e1 é alocado para 011110111111, então q[ e1 ] = 4 )
    q = [0 for _ in range(e.k)]
    
    #Preenchendo a lista q
    for k in range(e.k):
        for i in range(e.n-3):
            if (1 == e.string[i+(e.n*k)]) and (1 == e.string[i+(e.n*k)+1]) and (1 == e.string[i+(e.n*k)+2]) and (1 == e.string[i+(e.n*k)+3]):
                q[k] = q[k] + 1
    
    # A avaliação é a soma dos elementos de 
    aval = sum(q)
    
    return aval


# In[7]:


# RESTRIÇÃO 4 : 'Enfermeiros preferem consistência em seus horários, ou seja, eles preferem
#               trabalhar todos os dias da semana no mesmo turno (dia, noite, ou madrugada)'. 

# ENTRADA: Estado e
# SAÍDA:   Avaliação do estado e com base na restrição 4
def g_restricao04( e ):
    
     # Iniciando uma lista zerada que:
     #    Para cada enfermeiro ek, seja lM(ek) = número de alocações do enfermeiro ek para o turno 'Manhão'
     #                                  lN(ek) = número de alocações do enfermeiro ek para o turno 'Noite'
     #                                  lm(ek) = número de alocações do enfermeiro ek para o turno 'madrugada',
     # então q[ ek ] = 1 - ( max(lM,lN,lm) / (lM+lN+lm) )
    q = [0 for _ in range(e.k)]
    
    #Preenchendo a lista q
    for k in range(e.k):
        lM = 0
        p = 0
        while (p < e.n):
            lM = lM+e.string[ k*e.n + p ]
            p = p + 3
        lN = 0
        p = 1
        while (p < e.n):
            lN = lN+e.string[ k*e.n + p ]
            p = p + 3
        lm = 0
        p = 2
        while (p < e.n):
            lm = lm+e.string[ k*e.n + p ]
            p = p + 3
        if( sum([lM,lN,lm]) != 0 ):
            q[k] = 1-(max(lM,lN,lm)/sum([lM,lN,lm]))
        else:
            q[k] = 0
            
    # A avaliação é a soma dos elementos de q
    aval = sum(q)
    
    return aval


# # Função de Avaliação / Heurística

# In[8]:


# FUNÇÃO DE AVALIAÇÃO

# ENTRADA: Estado e
# SAÍDA:   Avaliação do estado e com base nas 4 restrições
def g( e ):
    return g_restricao01( e ) + g_restricao02( e ) + g_restricao03( e ) + g_restricao04( e )


# # Vizinhança

# In[9]:


# FUNÇÃO VIZINHOS

# ENTRADA: Estado e
# SAÍDA:   Lista com os vizinhos de e
def vizinhos( e ):
    
    # Criando uma lista com (e.k*e.n) cópias do estado e
    v = [ Estado(k = e.k, n = e.n, string = list.copy(e.string)) for _ in range(e.k*e.n) ]
    
    # Alterando o índice i da string contida em v[i]
    for i in range(e.k*e.n):
        if( v[i].string[i] == 0 ):
            v[i].string[i] = 1
        elif( v[i].string[i] == 1 ):
            v[i].string[i] = 0
   
    return v


# # Técnicas de Busca

# ### Simulated Annealing / Têmpera Simulada 

# In[10]:


#Classe que implementa a Têmpera Simulada
class TemperaSimulada( object ):
    
    #Construtor
    #  Entrada : inicial -> estado inicial para a busca
    #            energia -> função para cálculo de energia
    #            temperatura -> temperatura inicial
    #            iterativo -> Se o algoritmo reinicia a temperatura ao chegar em zero
    def __init__( self, inicial, energia, temperatura = 350, iterativo = False ):
        self.inicial = inicial
        self.temperatura = temperatura
        self.energia = energia
        self.iterativo = iterativo
        
    #Solve
    #  Saída: solução para o problema
    def solve( self, n_iteracao=1000 ):
        
        #Definindo a solução como o estado inicial
        solucao = self.inicial
        
        #A solução inicial será a melhor
        best = solucao
        
        #Inciando a temperatura com o valor da temperatura inicial
        temperatura = self.temperatura
        
        #Iterando de acordo com o número de iterações informado
        for j in range(n_iteracao):

            #Mostrando a população atual
            print("\t \033[46m Iteração ", j+1, "\033[0;0m \n" )
            print("\t \033[46m Temperatura", temperatura, "\033[0;0m \n" )
            print("\033[32m Solução: \033[0;0m \n")
            print(solucao.string,"\n")
            
            #Selecionando um dos vizinhos de forma aleatória utilizando a função choice
            vizinho = choice( vizinhos(solucao) )
            
            print("\033[32m Vizinho selecionado: \033[0;0m \n")
            print(vizinho.string,"\n")
            
            #Cálculo do delta
            deltaE = self.energia( vizinho ) - self.energia( solucao )
            
            print("\033[32m DeltaE: \033[0;0m \n")
            print(deltaE,"\n")
            
            #Se o delta for menor que zero, aceita ele como resposta
            if deltaE < 0:
                print(" DeltaE < 0, Vizinho escolhido como solução \n")
                solucao = vizinho
            #Caso contrário, é calculado a probabilidade de acordo com as especificações da técnica
            else:
                print(" DeltaE > 0, ")
                p = uniform(0,1)
                if p < exp(-deltaE/temperatura):
                    print("porém o Vizinho foi escolhido como solução")
                    solucao = vizinho
                else:
                    print("Vizinho não escolhido como solução")
            #Atualizando, caso necessário, a melhor solução
            if self.energia(best) > self.energia(solucao):
                best = solucao
            
            if temperatura > 1:
                temperatura = temperatura - 1
            #Se o algoritmo for iterativo, reinicializar a temperatura
            elif self.iterativo:
                temperatura = self.temperatura
            else:
                break
                
        #Retornando a melhor solução 
        return best


# ### Algoritmo Genético

# In[11]:


#Classe que implementa um Algoritmo Genético Simples

class AlgoritmoGenetico( object ):
    
    #Construtor
    #  Entrada : fitness -> função para cáculo de fitness dos cromossomos
    #            tam_populacao -> tamanho da população em cada geração
    #            num_geracoes -> número de gerações/iterações
    #            mutacao -> probabilidade de mutação de um cromossomo
    #            eletismo -> porcentagem de eletismo
    #            *parâmetros específicos do problema*
    #            k e n
    #
    def __init__( self, fitness, tam_populacao = 40, num_geracoes = 120,
                  mutacao = 0.05, eletismo = 0.25, k=10, n=21):
        
        #Nessa função estamos apenas inicializando as variáveis da classe
        self.k = k
        self.n = n
        
        self.cromo = Estado
        
        self.fitness = fitness
        
        self.tam_populacao = tam_populacao
        
        self.num_geracoes = num_geracoes
        
        self.mutacao = mutacao
        
        self.eletismo = eletismo
        
        
    #Crossover
    #  Entrada: Dois cromossomos (cromo1 e cromo2)
    #  Saída: Dois cromossomos (f1 e f2) frutos do crossover de cromo1 com cromo2
    def crossover(self, cromo1, cromo2 ):
    
        #Número de genes dos cromossomos pais
        tam = self.n*self.k
        
        #Gerando um ponto de crossover aleatório com a função randint 
        ponto = randint(1, tam-1)
        
        print("\033[31m Ponto de crossover : \033[0;0m",ponto)
    
        #Dividindo o cromo1 em duas partes de acordo com o ponto de crossover gerado
        cromo1A = cromo1.string[0:ponto]
        cromo1B = cromo1.string[ponto:]
    
        #Dividindo o cromo2 em duas partes de acordo com o ponto de crossover gerado
        cromo2A = cromo2.string[0:ponto]
        cromo2B = cromo2.string[ponto:]
    
        #Criando um novo cromossomo f1 filho de cromo1A com cromo2B
        f1 = self.cromo( k = cromo1.k, n = cromo1.n, string = cromo1A+cromo2B )
        #Criando um novo cromossomo f2 filho de cromo2A com cromo1B
        f2 = self.cromo( k = cromo1.k, n = cromo1.n, string = cromo2A+cromo1B )
    
        #Retornando os filhos
        return ( f1 , f2 )
    
    #Popular
    #  Saída: uma população de cromossomos inicial
    def popular(self):
        
        p = []
        for _ in range(self.tam_populacao):
            #A classe cromo/Estado gera aleatoriamente uma lista de genes/bits
            p.append( self.cromo(n=self.n,k=self.k) )
            
        #Retorna uma população inicial aleatória
        return p
    
    #Fitness População
    #  Entrada: população de cromossomos
    #  Saída: lista com o valor de fitness de cada membro da população
    def fitness_populacao( self, populacao ):
        
        f = []
        for c in populacao:
            #Para cada cromossomo na população é calculado o seu fitness e adicionado na lista
            f.append( self.fitness(c) )
            
        #Retorna o fitness da população
        return f
    
    #Realizar Mutação
    #  Entrada: um cromossomo/Estado
    #  Saída: cromossomo mutante
    def realizar_mutacao( self, cromo ):
        
        #Escolhendo o gene mutante de forma aleatória usando o randint
        gene = randint(0,cromo.tam()) - 1
        
        #Realizando a mutação no cromossomo, ou seja, alterando o valor do gene
        if( cromo.string[gene] == 0 ):
            cromo.string[gene] = 1
        else:
            cromo.string[gene] = 0
            
        #Retornando o cromossomo alterado
        return cromo
    
    #Elite
    #  Entrada: lista com os fitness de uma população
    #  Saída:  lista com os indices da elite da população/cromossomos com menor fitness
    def elite( self, fit ):
        
        #Definindo o tamanho da elite
        n_elite = int( self.eletismo * self.tam_populacao )
        
        #Criando lista que guardará o index da elite na população
        elite_index = []
        
        #Criando uma cópia da função fit para criar um heap de mínimo
        heap_fit = list.copy( fit )
        heapify( heap_fit )
        
        for _ in range(n_elite):
            
            #Retirando o menor fitness do heap
            menor = heappop( heap_fit )
            #Adicionando na lista da elite o index do elemento com o menor valor
            elite_index.append( fit.index(menor) )
         
        #Retornando a lista com o índice da elite
        return elite_index
        
    #Solve
    #  Saída: solução para o problema
    def solve( self ):
        
        #Criando população inicial
        populacao = self.popular()
        
        #Iterando de acordo com o número de gerações
        for j in range(self.num_geracoes):
            
            #Calculando o fitness da população inicial
            fit = self.fitness_populacao( populacao )
            
            #Definindo a próxima geração
            populacao2 = []
            
            #Mostrando a população atual
            print("\t \033[46m Geração ", j+1, "\033[0;0m \n" )
            print("\033[32m População: \033[0;0m \n")
            for i in range(len(populacao)):
                print("\033[31m Cromo ",i," \033[0;0m",populacao[i].string,"\n \033[31m Fit: ",fit[i],"\033[0;0m \n")
            print("\n")
            print("População gerada. Agora vamos aplicar o eletismo")
            print("\n")
            
            #Pegando os indices da elite
            elite_index = self.elite(fit)
            
            #Mostrando a elite
            print("\033[32m Elite: \033[0;0m")
            for i in elite_index:
                populacao2.append( populacao[i] )
                print("\033[31m Cromo ",i," \033[0;0m",populacao[i].string,"\n \033[31m Fit: ",fit[i],"\033[0;0m \n")
            
            print("\n")
            print("\033[32m Crossovers: \033[0;0m")
            
            #Iterando enquanto o limite do tamanho da população não for violado
            while( len(populacao2) <= self.tam_populacao ):
              
                #Escolhendo os cromossomos para crossover usando a função choices. Na função choices é possível
                #definir os pesos dos valores no sorteio. Porém, os pesos precisam ser positivos e queremos que
                #os fitness menores tenham maior peso.
                
                #Definindo os pesos para a função choice, para que o menor valor de fit tenha maior peso
                pesos = list(map(lambda x: max(fit) - x ,fit))
                
                #Sorteando os cromossomos
                cromo1 = populacao[ choices( range(self.tam_populacao), pesos )[0] ]
                cromo2 = populacao[ choices( range(self.tam_populacao), pesos )[0] ]
                
                print("\n \033[31m Cromo 1: \033[0;0m", cromo1.string)
                
                #Caso o cromo2 seja igual ao cromo1, sortie um novo cromossomo
                while(cromo1 == cromo2 ):
                    cromo2 = populacao[ choices( range(self.tam_populacao), pesos )[0] ]
                
                print("\n \033[31m Cromo 2: \033[0;0m",cromo2.string)
                
                #Crossover dos cromossomos
                (f1,f2) = self.crossover(cromo1,cromo2)
                
                #Mostrando os filhos de cromo1 com cromo2
                print("\n \033[31m Filho1 : \033[0;0m",f1.string)
                print("\n \033[31m Filho2 : \033[0;0m",f2.string,"\n")
                
                #Adicionando os filhos na população
                populacao2.append(f1)
                if( len(populacao2) < self.tam_populacao):
                    populacao2.append(f2)
                if( len(populacao2) == self.tam_populacao ):
                    break
            
            #Substituindo a antiga população pela nova
            populacao = list.copy( populacao )
            
            #Mutação
            for i in range(self.tam_populacao):
                
                #Aplicando a mutação nos cromossomos de acordo com a probabilidade
                pm = uniform(0,1)
                if( pm <= self.mutacao ):
                    print("\n \033[32m Mutação no Cromo ",i," da nova geração!!! \033[0;0m\n")
                    populacao[i] = self.realizar_mutacao( populacao[i] )
                    print(populacao[i].string,"\n")
        
        #Retornando a melhor solução, aquela com menor valor de fitness         
        return populacao[ fit.index( min(fit) ) ]


# In[14]:


k = int(input("\033[31m Informe o número de enfermeiros: \033[0;0m"))

print("Deseja informar a string de bits?\n")
w = input("Digite \033[31m Sim/SIM/sim \033[0;0m ou \033[31m Nao/NAO/nao \033[0;0m")

string = []
        
if( w in ["Sim","SIM","sim"] ):
            
    print("Digite os 21 bits de cada ENTER separados por espaço: \n ")
    for i in range(k):
        bits = (input("ENFER "+str(i)+":")).split()
        bits = list( map( lambda x: int(x), bits ) )
        string = string + bits
                
estado = Estado(k=k,string=string)

print("\n ~('-'~) Digite \033[31m 1 \033[0;0m para executar a \033[31m Têmpera Simulada \033[0;0m")
print(" ~('-'~) Digite \033[31m 2 \033[0;0m para executar a \033[31m Têmpera Simulada Iterativa \033[0;0m")
print(" ~('-'~) Digite \033[31m 3 \033[0;0m para executar a \033[31m Algoritmo Genético \033[0;0m")
    
op = str(input("\033[31m Escolha uma opcão: \033[0;0m"))
   
print("\n")
    
if op == '1':
    
    print("\n ~('-'~) Deseja informar:")
    print(" ~('-'~) 1 - \033[31m Temperatura \033[0;0m")
    print(" ~('-'~) 2 - \033[31m Número de iterações \033[0;0m")
    w = input("Digite \033[31m Sim/SIM/sim \033[0;0m ou \033[31m Nao/NAO/nao \033[0;0m")
    n_iteracoes = 1000
    if( w in ["Sim","SIM","sim"] ):
        temperatura = float(input("Temperatura: "))
        n_iteracoes = int(input("Número de iterações: "))
        ts = TemperaSimulada(inicial=estado, energia=g, temperatura = temperatura)
    else: 
        ts = TemperaSimulada(inicial=estado, energia=g)
        
    solucao = ts.solve(n_iteracao=n_iteracoes)
    
if op == '2':
    
    print("\n ~('-'~) Deseja informar:")
    print(" ~('-'~) 1 - \033[31m Temperatura \033[0;0m")
    print(" ~('-'~) 2 - \033[31m Número de iterações \033[0;0m")
    w = input("Digite \033[31m Sim/SIM/sim \033[0;0m ou \033[31m Nao/NAO/nao \033[0;0m")
    n_iteracoes = 1000
    if( w in ["Sim","SIM","sim"] ):
        temperatura = float(input("Temperatura: "))
        n_iteracoes = int(input("Número de iterações: "))
        ts = TemperaSimulada(inicial=estado, energia=g, temperatura = temperatura, iterativo = True)
    else: 
        ts = TemperaSimulada(inicial=estado, energia=g, iterativo=True)
        
    solucao = ts.solve(n_iteracao=n_iteracoes)
    
        
if op == '3':
    
    print("\n ~('-'~) Deseja informar: ")
    print(" ~('-'~) 1 - \033[31m Tamanho da população \033[0;0m")
    print(" ~('-'~) 2 - \033[31m Número de gerações \033[0;0m")
    print(" ~('-'~) 3 - \033[31m Mutação \033[0;0m")
    print(" ~('-'~) 4 - \033[31m Eletismo \033[0;0m")
    w = input("Digite \033[31m Sim/SIM/sim \033[0;0m ou \033[31m Nao/NAO/nao \033[0;0m")
    
    if( w in ["Sim","SIM","sim"] ):
        
        tam_populacao = int(input("Tamanho da população: "))
        num_geracoes = int(input("Número de gerações: "))
        mutacao = float(input("Mutação: "))
        eletismo = float(input("Eletismo: "))
        
        ag = AlgoritmoGenetico(fitness=g, tam_populacao = tam_populacao, num_geracoes = num_geracoes,
                           mutacao = mutacao, eletismo = eletismo, k=k)
    else: 
        ag = AlgoritmoGenetico(fitness=g, k=k)
    
    solucao = ag.solve()
    
    
print("\n \033[32m")
print("Solução Encontrada: ")
Visualizar_Estado(solucao)
print("Avaliação : ",g(solucao))
print('\033[0;0m')







