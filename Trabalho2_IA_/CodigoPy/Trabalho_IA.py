#!/usr/bin/env python
# coding: utf-8

# # Equipe
# ### Nome: Alessandro Souza Silva       Mat: 399941
# ### Nome: Diego Gaspar da Cruz         Mat: 398326

# A equipe escolheu representar as alocações como uma string de bits que em python é representado como uma lista de bits

# In[1]:


from heapq import * # Estrutura auxiliar na implementação da técnica 'Busca pelo Melhor Primeiro'
from random import randint # Méto+do para gerar valor aleatório

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

# ### Subida de Encosta Simples

# In[10]:


def Subida_Encosta_Simples( e ):
    
    print('\n\t'+'\033[31m'+'Estado Atual'+'\033[0;0m')
    print('\033[46m')
    Visualizar_Estado(e)
    print('\033[0;0m')
    print('\033[32m'+'Avaliação: ' + str(g(e)) + '\033[0;0m' +'\n')
    
    #Para cada vizinho v do estado atual
    for v in vizinhos(e):

        print('\n\n'+'\033[31m'+'Vizinho : '+'\033[0;0m')
        Visualizar_Estado(v)
        print('\033[31m'+'Avaliação do vizinho: '+'\033[0;0m'+str(g(v)))
        
        #Se v possui uma avaliação melhor, então executar a busca em v
        if( g(v) < g(e) ):
            print("Avaliação é menor, vizitar esse vizinho","\n","\n")
            return Subida_Encosta_Simples( v )
        
        print("Avaliação é maior, ignorar vizinho")
    
    print("\nEstado atual é o melhor")
    
    return e


# ### Subida de Encosta pelo Maior Aclive

# In[11]:


def Subida_Encosta_Maior_Aclive( e ):
    
    print('\n\t'+'\033[31m'+'Estado Atual'+'\033[0;0m')
    print('\033[46m')
    Visualizar_Estado(e)
    print('\033[0;0m')
    print('\033[32m'+'Avaliação: ' + str(g(e)) + '\033[0;0m' +'\n')
    
    melhor_g = 100000000000 # guarda a melhor avaliação encontrada
    melhor_v = -1 # guarda o indice do melhor vizinho
    
    for i,v in enumerate(vizinhos(e)):
        
        print('\n\n'+'\033[31m'+str(i)+'º Vizinho : '+'\033[0;0m')
        Visualizar_Estado(v)
        print('\033[31m'+'Avaliação do vizinho: '+'\033[0;0m'+str(g(v)))
        
        if( g(v) < melhor_g ):
            melhor_g = g(v)
            melhor_v = i
            
    print("\nAvaliação do melhor vizinho ",str(melhor_g)," indice ",str(melhor_v))
    if( melhor_g < g(e) ):
        print("Avaliação é menor, vizitar esse vizinho","\n","\n")
        return Subida_Encosta_Maior_Aclive( vizinhos(e)[melhor_v] )
    print("Estado atual é o melhor")
    return e


# ### *Subida de Encosta pelo Maior Aclive N

# In[12]:


def Subida_Encosta_Maior_Aclive_N( k=10, n=21, N=5 ):
    
    resultados = []
    for i in range(N):
        print("\n \033[46m                       " + 'INTERAÇÃO '+ str(i) + "                       \033[0;0m \n" )
        solucao = Subida_Encosta_Maior_Aclive( Estado( k=k, n=n ) )
        resultados.append(  ( g( solucao ), solucao )  )
    
    for i in range(N):
        print( "\n\nINTERAÇÃO ", i," AVALIAÇÃO: ", resultados[i][0] )
        print("\n \033[32m")
        print("Solução Encontrada: ")
        Visualizar_Estado(resultados[i][1])
        print('\033[0;0m')
    
    return min( resultados )[1]    
    


# ### Busca Pelo Melhor Primeiro

# In[13]:


#Implementação da fila de prioridade

class Fila_Prioridade( object ):
    
    def __init__(self):
        self.h = []
        
    def inserir( self, estado ):
        heappush(self.h, (g(estado), estado))
    
    def primeiro( self ):
        return self.h[0][1]
    
    def remove( self ):
        return heappop(self.h)[1]
        
    def vazia( self ):
        return len(self.h) == 0


# In[14]:


def Busca_Melhor_Primeiro( e, n_interacoes = 1000 ):
    
    #Criação da fila de prioridade
    fila = Fila_Prioridade()
        
    fila.inserir(e)
    
    #O melhor estado inicialmente será o estado inicial
    melhor_estado = e
    
    print('\033[46m')
    Visualizar_Estado(melhor_estado)
    print('\033[0;0m')
    print('\033[32m'+'Avaliação: ' + str(g(melhor_estado)) + '\033[0;0m' +'\n')
    
    #Enquanto a fila não estiver vazia ou o número de interações não ultrapassar o limite
    while (not fila.vazia())and(n_interacoes>0):
        #Retira o estado com melhor avaliação
        v = fila.remove()
        
        #Se a avaliação de v for a melhor então atualizar para v a melhor avaliação
        if (g(v) < g(melhor_estado)):
            melhor_estado = v
            print('\033[46m')
            Visualizar_Estado(melhor_estado)
            print('\033[0;0m')
            print('\033[32m'+'Avaliação: ' + str(g(melhor_estado)) + '\033[0;0m' +'\n')
            
        #Para cada vizinho u de v
        for u in vizinhos(v):
            #Se a avaliação de u for menor, então adicionar na fila
            if(g(u) < g(v)):
                fila.inserir(u)
                
        n_interacoes = n_interacoes-1
        
    return melhor_estado


# In[15]:


k = int(input("\033[31m Informe o número de enfermeiros: \033[0;0m"))

print("Deseja informar a string de bits?\n")
w = input("Digite \033[31m Sim/SIM/sim \033[0;0m ou \033[31m Nao/NAO/nao \033[0;0m")

string = []
        
if( w in ["Sim","SIM","sim"] ):
            
    print("Digite os 21 bits de cada ENFER separados por espaço: \n ")
    for i in range(k):
        bits = (input("ENFER "+str(i)+":")).split()
        bits = list( map( lambda x: int(x), bits ) )
        string = string + bits
                
estado = Estado(k=k,string=string)

print("\n ~('-'~) Digite \033[31m 1 \033[0;0m para executar a \033[31m Subida de Encosta Simples \033[0;0m")
print(" ~('-'~) Digite \033[31m 2 \033[0;0m para executar a \033[31m Subida de Encosta pelo Maior Aclive \033[0;0m")
print(" ~('-'~) Digite \033[31m 3 \033[0;0m para executar a \033[31m Busca pelo Melhor Primeiro \033[0;0m")
print(" ~('-'~) Digite \033[31m 4 \033[0;0m para executar a \033[31m Subida de Encosta pelo Maior Aclive N \033[0;0m")
    
op = str(input("\033[31m Escolha uma opcão: \033[0;0m"))
   
print("\n")
    
if op == '1':
                
    solucao = Subida_Encosta_Simples(estado)
        
if op == '2':
    
    solucao = Subida_Encosta_Maior_Aclive(estado)
    
if op == '3':
    
    solucao = Busca_Melhor_Primeiro(estado)
    
if op == '4':
    
    N = int( input("Informe o valor de N: ") )
    solucao = Subida_Encosta_Maior_Aclive_N(k=k,N=N)
    
print("\n \033[32m")
print("Solução Encontrada: ")
Visualizar_Estado(solucao)
print("Avaliação : ",g(solucao))
print('\033[0;0m')


# In[ ]:




