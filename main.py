import random
import math
import time

#funcao que recebe uma lista de tabuleiros e a quantidade de rainhas
#cria um array com N rainhas colocadas aleatoriamente, e devolve o array
def create_board(n_queens):
    board =[x for x in range(n_queens)]#funcao que gera uma lista de numeros de 0 a N
    random.shuffle(board) # funcao que bagunça uma lista

    return board


#funcao que rece um tabuleio, e as cordenadas de uma rainha, e retorna a quantidade de colisoes, para frente, que aquela rainha possui
def is_safe(board):

    crashs = 0
    atual = 1
    n_queens = len(board)
    for x in board:
        i=1
    # Check for queens in the diagonal
        for j in range(atual, n_queens):
            if (x+i) == board[j]:
                crashs+=1
            
            if (x-i) == board[j]:
                crashs +=1
            
            i += 1
        atual += 1

    return crashs


#funcao que imprime um tabuleiro
def print_board(board):
    n_queens = len(board)
    imprimir = [[0 for _ in range(n_queens)]for _ in range(n_queens)]

    for (x,i) in zip(board,range(n_queens)):
        imprimir[i][x]=1

    for row in imprimir:
        print(" ".join(map(str, row)))



#funcao que recebe uma lista com o numero de colisoes dos tabuleiros e o numero de parentes escolhido pelo usuario
#Retorna uma lista com a posicao dos N tabuleiros com menas colisoes, que seram os novos pais da proxima geracao
def chose_parents(colisions,n_parents):
    colisions_ord = colisions.copy() #copia a lista de colisoes para nao alterar a original
    colisions_rem = colisions.copy() #copia a lsita de colisoes para nao alerar a origial
    colisions_ord.sort() #ordena a lista de colisoes em ordem crescente
    parents =[]
    repetitons=[]

    #pega o index original dos N primeiros elementos da lista ordenada 
    for i in range(n_parents):
       #Cria uma lista com os tabuleiros com o mesmo numero de colisoes e caso tenha repeticoes escolhe aleatoriamente entre eles
       repetitons = [y for x,y in zip(colisions_rem, range(len(colisions))) if x == colisions_ord[i]]
       if len(repetitons) ==1:
           parents.append(repetitons[0])
       else:
           parent = random.sample(repetitons, 1)
           parents.append(parent[0])
       #troca o valor da colisao na lista de colisoes, para evitar repetir o index, de dois tabuleiros com mesmo numero de colisoes
       colisions_rem[parents[i]] = math.inf 

    return parents

    

#funcao que recebe uma lista de tabuleiros, os pais escolhidos,e numero de rainhas
#gera novos filhos cruzando dois pais, da lista de pais escolhidos, e substitui um tabuleiro nao pai da tabela de tabuleiros
def gen_childs(boards, parents,n_queens):
    

    for i in range(len(boards)):
        if i in parents: # verifica se o tabuleiro que esta na posicao i da lista de tabuleiros, nao e um tabuleiro pai
            continue
        
        chosens= random.sample(parents, 2) #Escolhe aleatoriamente dois pais da lista de pais
        parent1= boards[chosens[0]] #pega da lista de tabueliros,os pais escolhidos
        parent2= boards[chosens[1]]
        
        cycle = [False] * n_queens #gera uma lista de para marcar as posicoes que ja foram preenchidas
        child = [None] * n_queens #gera um filho nao preenchido

        # Encontra o primeiro ciclo
        start = random.randint(0, n_queens - 1) #Gera o inicio do ciclo
        while not cycle[start]: #enquanto nao fecha o ciclo continua
            cycle[start] = True
            child[start] = parent1[start] # faz o valor do filho na pos start ser igual ao do pai 1 na pos start
            start = parent2.index(parent1[start]) #pega a pos no pai2 do valor do pai 1 na posicao start, que vira o novo start 

        # Preencha os valores restantes com o pai 2
        for j in range(n_queens):
            if not cycle[j]:
                child[j] = parent2[j]

        boards[i]= child

    return parents




#funcao que recebe uma lista de tabuleiro,os pais escolhidos , numero de rainhas e a chance da mutacao
#E gera mutatoes nos tabuleiros filhos em com uma probabilidade = mutante_chance
#tambem corrigi o numero de rainhas nos filhos, que durante a combinacao dos parentes podem ser gerados com menos de N rainhas
def mutation_childs(boards, parents,n_queens,mutate_chance =50):
    n_matrix= n_queens * n_queens
    for i in range(len(boards)):
        if i in parents:
            continue
        
        child= boards[i]
    
     #gera um numero aletorio de 0 a 99 e se for > que mutante_chance, ele nao gera a mutacao
        if  random.randrange(100) > mutate_chance:
            continue

     #Se o numero gerado for menor que mutate_chance, escolhe aleatoriamente a posicao de uma rainha e retira ela
        chosens= random.sample(range(n_queens),2)
        swap = child[chosens[0]]
        child[chosens[0]] = child[chosens[1]]
        child[chosens[1]] = swap 

         




    

def eight_queens():
    start_time = time.time()
    n_queens= 8      #Tamanho do problema, numero de rainhas
    n_parents = 5    #Numero de tabuleiros pais que seram escolhidos
    max_gen= 10000    #Numero maximo de geracoes
    n_boards= 11     #Numero de tabuleiros por geracao
    mutate_chance = 50 #Chance de mutacao
    boards=[]
    colisions_initial=[]
    colisions=[]

 #cria populacao inicial
    for i in range(n_boards):
        board =create_board(n_queens)
        print(f"Board inicial {i+1}",board)
        boards.append(board)
        print("Board", i+1)
        print_board(boards[i])
        print()
        colisions.append(is_safe(boards[i]))

    colisions_initial =colisions.copy()
    print(colisions)
    print()

   #loop das geracoes 
    for gen in range(max_gen):
        parents = chose_parents(colisions,n_parents)
        gen_childs(boards, parents,n_queens)
        mutation_childs(boards, parents,n_queens,mutate_chance)
        colisions.clear()
        for j in range(n_boards):
           colisions.append(is_safe(boards[j]))

        print("Gen: ",gen,"Colisions: ", colisions)
    #para se achar uma solucao
        if 0 in colisions:
            break



 #imprime ultima geracao
    for i in range(n_boards):
        print("New ",i+1)
        print_board(boards[i])
        print()

    print("Initial Colisions: ", colisions_initial)
    print("Final Colisions: ", colisions)
    print()

    index_winner = chose_parents(colisions,n_parents) #pega melhor resultado

    print("Best :", index_winner[0]+1," of gen : " ,gen+1)
    print_board(boards[index_winner[0]])
    print()
    end_time = time.time()
    waiting_time = end_time - start_time
    print("Waiting time: ", waiting_time, "s")

    return (waiting_time, gen+1)

def executeN(n):
    (time_atual,gens_atual) = eight_queens()
    time_sum = time_atual
    gens = gens_atual
    for _ in range(n-1):
        (time_atual,gens_atual) = eight_queens()
        time_sum += time_atual
        gens += gens_atual


    print("Media de tempo de ", n, " execucoes eh: ", time_sum / n)
    result = "Media de tempo de " + str(n) + " execucoes eh: " + str((time_sum/n)) + "\n"
    print("Media de Geracoes de ", n, " execucoes eh: ", gens / n)
    result += "Media de Geracoes de " + str(n) + " execucoes eh: " + str((gens/n)) + "\n"

    with open("resultCE.txt", "a") as arquivo:
        arquivo.write(result)

executeN(100)