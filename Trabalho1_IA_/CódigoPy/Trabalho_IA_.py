#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Sobre a modelagem do problema das 'N Rainhas':
#
#        Estados de Busca: 
#          * Um estado é representado por uma lista 'tabuleiro' de inteiros de tamanho até n
#          * Os valores de 'tabuleiro' estão entre [-1,n-1], sem repetição
#          * tabuleiro[i] = j, significa que na linha i e coluna j existe uma rainha (exceção j=-1)
#          * tabuleiro[i] = -1, significa que na linha i não contém nenhuma rainha
#        Operações:
#          * Adicionar uma rainha na primeira linha que não contém uma rainha, sem que ocorra ataques
#        Estado Objetivo:
#          * tabuleiro[i] diferente de '-1' para todo i em [0,n-1]


# In[2]:


#Implementação da FILA

class Fila(object):
    #Construtor
    def __init__(self):
        self.dados = []
        
    #Inserir : insere elemento na Fila
    def insere(self, elemento):
        self.dados.append(elemento)
 
    #Retirar : retira e retorna o primeiro elemento da Fila
    def retira(self):
        return self.dados.pop(0)
 
    def primeiro(self):
        return self.dados[0]

    #Vazia : verifica se a Fila está vazia
    def vazia(self):
        return len(self.dados) == 0


# In[3]:


#Implementação da Pilha

class Pilha(object):
    #Construtor
    def __init__(self):
        self.dados = []
 
    #Empilhar : insere elemento na Pilha
    def empilha(self, elemento):
        self.dados.append(elemento)
 
    def top(self):
        if not self.vazia():
            return self.dados[-1]

    #Desempilhar : retira e retorna o último elemento da Pilha
    def desempilha(self):
        if not self.vazia():
            return self.dados.pop(-1)
 
    #Vazia : verifica se a Pilha está vazia
    def vazia(self):
        return len(self.dados) == 0


# In[4]:


# Classe Estado : representa um estado possível do problema das 'N Rainha'
#                 *Atributos: 
#                   'n' - Número de rainhas
#                   'tabuleiro' - Lista que representa a configuração do tabuleiro
#
#                 *Métodos:
#                   'validaOperacao(i,j)' - Retorna 'True', caso inserir uma rainha na linha i
#                                           e coluna j não coloca outra rainha em risco.
#                                           Retorna 'False', caso contrário
#                   'isObjetivo()' - Retorna 'True', caso o estado seja um estado objetivo.
#                                    Retorna 'False', caso contrário
#                   'gerarVizinhos(i)' - Retorna a lista de vizinhos do estado inserindo uma rainha
#                                        na linha i

class Estado(object):
    
    #Construtor
    def __init__(self, n):
        self.n = n
        self.tabuleiro = []
        
    def validaOperacao(self,i,j):
        #Para verificar se existe uma rainha é atacada pelas diagonais é verificado se existe uma soma i+j 
        #ou uma subtração i-j
        soma = []
        sub = []
        for i0 in range(self.n):
            if self.tabuleiro[i0] != -1:
                soma.append(i0+self.tabuleiro[i0])
                sub.append(i0-self.tabuleiro[i0])
        #Verificando se:
        #  -Já existe uma rainha na coluna j
        #  -Já existe uma rainha na diagonal principal
        #  -Já existe uma rainha na diagonal secundária
        if self.tabuleiro.count(j) > 0 or soma.count(i+j) > 0 or sub.count(i-j) > 0:
            return False
        return True
    
    def isObjetivo(self):
        #Pela modo como a programação do problema foi construida, um estado objetivo é aquele
        #em que todas as linhas possuem uma rainha (A ausência de uma rainha é representado pelo valor '-1')
        for i in range(self.n):
            if self.tabuleiro[i] == -1: #Se pelo menos uma linha contém '-1', o estado não é objetivo
                return False
        return True
    
    def gerarVizinhos(self, i):
        #Como dito anteriormente, essa função retorna todos os vizinhos válidos do estado, inserindo
        #uma rainha na linha i
        vizinhos = []
        for j in range(self.n): #Será testado todas as possibilidades de j (coluna)
            if self.validaOperacao(i,j):        #Caso inserir na linha i o valor j seja válido:
                aux = list.copy(self.tabuleiro)  #1-Fazer uma cópia do tabuleiro do estado
                aux[i] = j                       #2-Na cópia, inserir na linha i o valor j
                vizinhos.append(aux)             #3-Adicionar a cópia na lista de vizinhos válidos
        return vizinhos #Retorna a lista de vizinhos


# In[5]:


#Implementação da Busca em Profundidade(DFS) para o problema das 'N Rainhas'

def BFS( inicial ):

    n = inicial.n
    
    filaEstados = Fila() #Fila responsável por guardar informação sobre um caminho(lista de estados)
    filaIndices = Fila() #Fila responsável por guardar informação da próxima linha a ser preenchida
    #A ideia é que as filas tenham sempre o mesmo tamanho.
    
    filaEstados.insere( [inicial] ) #O caminho inicial é formado apenas pelo estado inicial
    filaIndices.insere( 0 ) #No caminho inicial, o último estado (o estado inicial) terá que 
                              #inserir um elemento na linha 0 

    ordemGerados = [ [inicial] ] #Lista para guardar a ordem em que os caminhos são gerados.
                                 #Inicialmente recebe o caminho inicial
    
    solucao = False #Variável para identificar se existe solução
    sair = False #Variável para identificar se precisa mostrar passo a passo
    
    while (not filaEstados.vazia()) :
        
        #--------------------- Apenas Interação ---------------------
        if not sair:
            print('\n\t'+'\033[31m'+'Estado da Fila'+'\033[0;0m')
            print('\033[32m'+'Número de elementos:'+'\033[0;0m'+str(len(filaEstados.dados)))
            print('\033[32m'+'Elemento do topo:'+'\033[0;0m')
            for x in filaEstados.primeiro():
                print('\033[46m'+str(x.tabuleiro)+'\033[0;0m')
            if str(input('Aperte ENTER para continuar ou digite E para sair')) == 'E':
                sair = True
        #---------------------------------------------------------------
                
        #Sobre as duas primeiras variáveis auxiliares:
        # aux1 contém um caminho
        # aux1[-1] é o último estado( última configuração do tabuleiro ) do caminho aux1
        # aux2 contém a linha onde deve ser inserido uma rainha em aux[-1]
        
        aux1 = filaEstados.retira()
        aux2 = filaIndices.retira()
        
        if( aux1[-1].isObjetivo() ): #Verificar se aux1[-1] é um objetivo
            solucao = True
            
            #--------------------- Apenas Interação ---------------------
            if not sair:
                print("\nElemento do topo é um objetivo !")
                if str(input('Aperte ENTER para continuar ou digite E para sair')) == 'E':
                    sair = True
            break
            #------------------------------------------
        
        else:
            
            #--------------------- Apenas Interação ---------------------
            if not sair:
                print("\nElemento do topo não é um objetivo. Hora de gerar seus vizinhos")
                if str(input('Aperte ENTER para continuar ou digite E para sair')) == 'E':
                    sair = True
            #------------------------------------------
            
        vizinhos = aux1[-1].gerarVizinhos(aux2) #Gerar os vizinhos de aux1[-1] que inserem
                                               #uma rainha na linha aux2
        
        #--------------------- Apenas Interação ---------------------
        if not sair:
            print('\033[32m'+'\nVizinhos: '+'\033[0;0m',vizinhos)
            print("Vamos adicioná-los na fila !")
            if str(input('Aperte ENTER para continuar ou digite E para sair')) == 'E':
                sair = True
        #------------------------------------------
        
        for v in vizinhos:              #Para cada vizinho:
            aux3 = Estado(n)            #1-Criar um novo estado aux3
            aux3.tabuleiro = v          #2-Definir o vizinho v como tabuleiro de aux3
            aux4 = (list.copy(aux1))    #3-Criar uma cópia aux4 de aux1 (cópia do caminho)
            aux4.append(aux3)           #4-Adicionar ao caminho aux4 o estado aux3
            ordemGerados.append(aux4)   #5-Registrar o momento em que foi gerado o novo caminho
            filaEstados.insere(aux4)  #6-Inserir o novo caminho na fila
            filaIndices.insere(aux2+1)#7-Inserir a informação da próxima linha que deve ser preenchida
    
    if not solucao:
        print("\nPoxa não tem solução")
        ordemGerados.append([inicial]) #Se não existe solução, coloca o estado inicial no final do gerados 
                                       #(É apenas um simbolismo que eu adotei)
    
    return ordemGerados #Retornar todos os caminhos. A solução será o último caminho


# In[6]:


#Implementação da Busca em Profundidade(DFS) para o problema das 'N Rainhas'

def DFS( inicial ):

    n = inicial.n
    
    pilhaEstados = Pilha() #Pilha responsável por guardar informação sobre um caminho(lista de estados)
    pilhaIndices = Pilha() #Pilha responsável por guardar informação da próxima linha a ser preenchida
    #A ideia é que as pilhas tenham sempre o mesmo tamanho.
    
    pilhaEstados.empilha( [inicial] ) #O caminho inicial é formado apenas pelo estado inicial
    pilhaIndices.empilha( 0 ) #No caminho inicial, o último estado (o estado inicial) terá que 
                              #inserir um elemento na linha 0 

    ordemGerados = [ [inicial] ] #Lista para guardar a ordem em que os caminhos são gerados.
                                 #Inicialmente recebe o caminho inicial
    
    solucao = False #Variável para identificar se existe solução
    sair = False #Variável para identificar se precisa mostrar passo a passo
    
    while (not pilhaEstados.vazia()) :
        
        #--------------------- Apenas Interação ---------------------
        if not sair:
            print('\n\t'+'\033[31m'+'Estado da Pilha'+'\033[0;0m')
            print('\033[32m'+'Número de elementos:'+'\033[0;0m'+str(len(pilhaEstados.dados)))
            print('\033[32m'+'Elemento do topo:'+'\033[0;0m')
            for x in pilhaEstados.top():
                print('\033[46m'+str(x.tabuleiro)+'\033[0;0m')
            if str(input('Aperte ENTER para continuar ou digite E para sair')) == 'E':
                sair = True
        #---------------------------------------------------------------
                
        #Sobre as duas primeiras variáveis auxiliares:
        # aux1 contém um caminho
        # aux1[-1] é o último estado( última configuração do tabuleiro ) do caminho aux1
        # aux2 contém a linha onde deve ser inserido uma rainha em aux[-1]
        
        aux1 = pilhaEstados.desempilha()
        aux2 = pilhaIndices.desempilha()
        
        if( aux1[-1].isObjetivo() ): #Verificar se aux1[-1] é um objetivo
            solucao = True
            
            #--------------------- Apenas Interação ---------------------
            if not sair:
                print("\nElemento do topo é um objetivo !")
                if str(input('Aperte ENTER para continuar ou digite E para sair')) == 'E':
                    sair = True
            break
            #------------------------------------------
        
        else:
            
            #--------------------- Apenas Interação ---------------------
            if not sair:
                print("\nElemento do topo não é um objetivo. Hora de gerar seus vizinhos")
                if str(input('Aperte ENTER para continuar ou digite E para sair')) == 'E':
                    sair = True
            #------------------------------------------
            
        vizinhos = aux1[-1].gerarVizinhos(aux2) #Gerar os vizinhos de aux1[-1] que inserem
                                               #uma rainha na linha aux2
        
        #--------------------- Apenas Interação ---------------------
        if not sair:
            print('\033[32m'+'\nVizinhos: '+'\033[0;0m',vizinhos)
            print("Vamos adicioná-los na pilha !")
            if str(input('Aperte ENTER para continuar ou digite E para sair')) == 'E':
                sair = True
        #------------------------------------------
        
        for v in vizinhos:              #Para cada vizinho:
            aux3 = Estado(n)            #1-Criar um novo estado aux3
            aux3.tabuleiro = v          #2-Definir o vizinho v como tabuleiro de aux3
            aux4 = (list.copy(aux1))    #3-Criar uma cópia aux4 de aux1 (cópia do caminho)
            aux4.append(aux3)           #4-Adicionar ao caminho aux4 o estado aux3
            ordemGerados.append(aux4)   #5-Registrar o momento em que foi gerado o novo caminho
            pilhaEstados.empilha(aux4)  #6-Empilhar o novo caminho na pilha
            pilhaIndices.empilha(aux2+1)#7-Empilhar a informação da próxima linha que deve ser preenchida
    
    if not solucao:
        print("\nPoxa não tem solução")
        ordemGerados.append([inicial]) #Se não existe solução, coloca o estado inicial no final do gerados 
                                       #(É apenas um simbolismo que eu adotei)
    
    return ordemGerados #Retornar todos os caminhos. A solução será o último caminho


# In[ ]:


n = int(input("Informe o número de rainhas/dimensão do tabuleiro: "))

inicial = Estado(n)

while True:
    
    inicial.n = n
    for _ in range(n):
        inicial.tabuleiro.append(-1)
        
    print(" Digite 1 para executar a BFS")
    print(" Digite 2 para executar a DFS")
    print(" Digite 3 para alterar o número de rainhas")
    print(" Dizite 4 para sair")
    
    op = str(input("Escolha uma opcão: "))
    
    print("\n")
    
    if op == '1':
        solucao = BFS(inicial)
        print("\n")
        print("Solução Encontrada: ")
        for e in solucao[-1]:
            print('\033[32m',e.tabuleiro,'\033[0;0m')
        print("\n")
    
    if op == '2':
        solucao = DFS(inicial)
        print("\n")
        print("Solução Encontrada: ")
        for e in solucao[-1]:
            print('\033[32m',e.tabuleiro,'\033[0;0m')
        print("\n")
        
    if op == '3':
        n = int(input("Informe o número de rainhas/dimensão do tabuleiro: "))
        
    if op == '4':
        break
    
    del inicial.tabuleiro[:]
    

