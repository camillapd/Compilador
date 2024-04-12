grafo = {'SA':[('S2','a'),('S3','b'),('S4','b')], 'SB': [('S5','a')]}

# print(grafo)

for k in grafo:
    print(k, 'k') # o estado    

for i in range(len(list(grafo.values()))):
    print(list(grafo.values())[i], 'i') # lista das transições de cada estado
    for j in range(len(list(grafo.values())[i])):
        print(list(grafo.values())[i][j], 'i, j') # tupla de cada transição individual

        print(list(grafo.values())[i][j][0], 'i,j,0') # o estado em que vai a transição
        print(list(grafo.values())[i][j][1], 'i,j,1') # o valor


# TODO
# for i in grafo:
#     print(list(grafo.keys())[i])

# remover a recurssão a esquerda / fatorar
# montar first follow 
# fazer a tabela de look ahead

# estado final é o nome do token
# o programa de saída que pede o código