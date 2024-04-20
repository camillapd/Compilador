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


afne = Automato()
afne.estado_inicial = 'S1'
afne.estados_finais.append('S3')
afne.automato = {'S1': [('S2', 'a'), ('S4,S2', 'e')],
                 'S2': [('S3', 'a'), ('S1,S3', 'e')],
                 'S3': [('S3', 'a')],
                 'S4': [('S4', 'a')]}

afn = Automato()

print(list, 'Fecho')

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

x = grafo.get("SA")











# TODO
# for i in grafo:
#     print(list(grafo.keys())[i])

# remover a recurssão a esquerda / fatorar
# montar first follow
# fazer a tabela de look ahead

# estado final é o nome do token
# o programa de saída que pede o código
