grafo = {'S1': [('S2', 'a'), ('S1', 'fecho')],
         'S2': [('S6', 'e'), ('S1,S2', 'fecho')]}


class Automato:
    def __init__(self):
        self.automato = {}
        self.estado_inicial = None
        self.estados_finais = []

    def add_estado(self, estado):
        if estado not in self.automato:
            self.automato[estado] = []

    def add_transicao(self, estado1, estado2, valor):
        self.automato[estado1].append((estado2, valor))


at_fecho = Automato()
at_fecho.estado_inicial = 'S1'
at_fecho.estados_finais.append('S3')
at_fecho.automato = {'S1': [('S2', 'a'), ('S1', 'fecho')],
                     'S2': [('S3', 'a'), ('S1,S2,S3', 'fecho')],
                     'S3': [('S3', 'fecho')]}

afn = Automato()

for estado in at_fecho.automato:
    afn.add_estado(estado)
    if estado == at_fecho.estado_inicial:
        afn.add_estado(at_fecho.automato.get(estado)[-1][0])
        afn.estado_inicial = at_fecho.automato.get(estado)[-1][0]
    if estado in at_fecho.estados_finais:
        afn.add_estado(estado)
        afn.estados_finais.append(estado)
    else:
        afn.add_estado(estado)

    # o valor do fecho do estado atual
    fecho_estado = at_fecho.automato.get(estado)[-1][0]
    # o símbolo da setinha que vou colocar para o novo estado do afn
    fecho_res = ""

    for j in range(len(at_fecho.automato.get(estado))-1):

        # checo se o valor do fecho é uma lista de estados
        # se for eu coloco os valores em uma lista e itero por eles
        if "," in fecho_estado:
            list_fecho = fecho_estado.split(",")
            for fecho in list_fecho:

                # aqui eu checo se tem mais de uma transição nesse estado
                # porque se tiver uma só é o fecho e não quero contar isso nas minhas setinhas
                if len(at_fecho.automato.get(fecho)) > 1:

                    # o destino é o valor da transição, para eu usar o fecho desse estado
                    fecho_destino = at_fecho.automato.get(fecho)[j][0]
                    um_fecho = at_fecho.automato.get(
                        fecho_destino)[-1][0]

                    # checagem para não colocar valores repetidos na transição nova
                    if um_fecho not in fecho_res:
                        # como tem mais de um estado em que estou olhando o fecho, aqui junto todos
                        fecho_res = um_fecho + fecho_res
        else:
            # aqui eu checo se tem mais de uma transição nesse estado
            # porque se tiver uma só é o fecho e não quero contar isso nas minhas setinhas
            if len(at_fecho.automato.get(fecho_estado)) > 1:
                fecho_destino = at_fecho.automato.get(fecho_estado)[j][0]
                fecho_res = at_fecho.automato.get(fecho_destino)[-1][0]

        afn.add_transicao(estado, fecho_res,
                          at_fecho.automato.get(estado)[j][1])

print(afn.automato)


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

# for k in grafo:
#     estado = k
#     print(estado)
#     for i in range(len(grafo.get(estado))):
#         print(grafo.get(estado)[i], 'i')
#         print(grafo.get(estado)[i][0],'j 0')
#         print(grafo.get(estado)[i][1], 'j 1')

x = grafo.get("SA")
# print(grafo.get("SA")[0][0])










# TODO
# for i in grafo:
#     print(list(grafo.keys())[i])

# remover a recurssão a esquerda / fatorar
# montar first follow
# fazer a tabela de look ahead

# estado final é o nome do token
# o programa de saída que pede o código
