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


# afne.automato = {'S1': [('S1,S2,S3,S5,S6,S9', 'a')],
#                  'S2': [('S1,S2,S3,S5,S6,S9,S10', 'a'), ('S1,S3,S4,S5,S6,S9', 'b')],
#                  'S3': [('S1,S3,S4,S5,S6,S9', 'b')],
#                  'S4': [('S1,S2,S3,S5,S6,S9,S10', 'a'), ('S1,S3,S4,S5,S6,S9', 'b')],
#                  'S5': [('S1,S2,S3,S5,S6,S9', 'a'), ('S1,S3,S4,S5,S6,S9', 'b')],
#                  'S6': [('S1,S2,S3,S5,S6,S9,S10', 'a'), ('S1,S3,S4,S5,S6,S9', 'b')],
#                  'S7': [('S1,S2,S3,S5,S6,S9,S10', 'a'), ('S1,S3,S4,S5,S6,S9', 'b')],
#                  'S9': [('S10', 'a')],
#                  'S10': [('S9', 'x')]}

afne = Automato()
afne.estado_inicial = 'S1'
afne.estados_finais.append('S4')
afne.automato = {'S1': [('S2', 'a')],
                 'S2': [('S3', 'a'), ('S1', 'b')],
                 'S3': [('S4', 'b')],
                 'S4': [('S4', 'a'), ('S4', 'b')]}

novo = "FIM"
novo_afne = Automato()

for estado in afne.automato:
    novo_afne.add_estado(novo)
    novo_afne.estados_finais.append(novo)
    if estado == afne.estado_inicial:
        novo_afne.estado_inicial = estado
    for j in range(len(afne.automato.get(estado))):
        estado_destino = afne.automato.get(estado)[j][0]
        if estado in afne.estados_finais:
            if estado_destino in afne.estados_finais:
                novo_afne.add_transicao(novo, novo, afne.automato.get(estado)[j][1])
            else:
                novo_afne.add_transicao(novo, estado_destino, afne.automato.get(estado)[j][1])
        else:
            novo_afne.add_estado(estado)
            if estado_destino in afne.estados_finais:
                novo_afne.add_transicao(estado, novo, afne.automato.get(estado)[j][1])
            else:
                novo_afne.add_transicao(estado, estado_destino, afne.automato.get(estado)[j][1])

# for estado in afne.automato:
#     if estado in afne.estados_finais:
#         afne.automato[novo] = afne.automato.pop(estado)
        # afne.add_transicao(novo,afne.automato.pop(estado))
    # for j in range(len(afne.automato.get(estado))):
    #     pass
    
print(novo_afne.automato)

afn = Automato()


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
