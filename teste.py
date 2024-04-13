grafo = {'SA': [('S2', 'a'), ('S3', 'b'), ('S4', 'b')], 'SB': [('S5', 'a')]}

# print(grafo)

# for k in grafo:
#     # print(k, 'k')  # o estado
#     for i in range(len(list(grafo.values()))):
#         # lista das transições de cada estado
#         # print(list(grafo.values())[i], 'i')
#         for j in range(len(list(grafo.values())[i])):
#             # tupla de cada transição individual
#             # print(list(grafo.values())[i][j], 'i, j')

#             # o estado em que vai a transição
#             # print(list(grafo.values())[i][j][0], 'i,j,0')
#             # print(list(grafo.values())[i][j][1], 'i,j,1')  # o valor

for k in grafo:
    estado = k
    print(estado)
    for i in range(len(grafo.get(estado))):
        print(grafo.get(estado)[i], 'i')
        print(grafo.get(estado)[i][0],'j 0')
        print(grafo.get(estado)[i][1], 'j 1')

x = grafo.get("SA")
print(grafo.get("SA")[0][0])

# TODO
# for i in grafo:
#     print(list(grafo.keys())[i])

# remover a recurssão a esquerda / fatorar
# montar first follow
# fazer a tabela de look ahead

# estado final é o nome do token
# o programa de saída que pede o código
