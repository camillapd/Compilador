class AFN:
    def __init__(self):
        self.afn1 = {}
        self.estado_inicial = None
        self.estados_finais = []

        # o afn é um afn1
        # é um dicionário no qual a chave é o vértice e os valores são listas de vértices
        # o vértice é um estado (e.g S1) e as listas de vértices são as transições (e.g S1->S2,S3)

    def add_estado(self, estado):
        if estado not in self.afn1:
            self.afn1[estado] = []

    def add_transicao(self, estado1, estado2, valor):
        if estado1 in self.afn1 and estado2 in self.afn1:
            self.afn1[estado1].append((estado2, valor))

    def add_finais(self, estado):
        if estado in self.afn1:
            self.estados_finais.append(estado)

    def print_afn1(self):
        print("Automato:", self.afn1)


def algoritmo_thompson(er):
    pilha = list(er)
    pilha.reverse()
    pilha_afn = []
    count = 1

    print(pilha)

    for i in range(0, len(pilha)):
        if pilha[i] == '.':
            afn1 = pilha_afn.pop()
            afn2 = pilha_afn.pop()
            afn = AFN()

            estado_final = 'S' + str(count+1)

            # TODO
            # iterar pelo afn1
            # adicionar estados e transições no afn novo
            for k in afn1:
                afn.add_estado(k)
                for v in afn1[k][v]:
                    afn.add_transicao(
                        estado_inicial, afn1.estado_inicial, 'e')

            # TODO
            # iterar pelo afn2
            # adicionar estados e transições no afn novo
            for k in afn2:
                afn.add_estado(k)
                for v in afn2[k][v]:
                    afn.add_transicao(
                        estado_inicial, afn2.estado_inicial, 'e')
                    # adicionar transição dos estados finais do afn2 no afn TODO
                    # afn.add_transicao(x, estado_final, 'e')

            # novo estado final
            afn.estados_finais.append(estado_final)

            pilha_afn.append(afn)
        elif pilha[i] == "*":
            afn1 = pilha_afn.pop()
            afn = AFN()

            estado_inicial = 'S' + str(count)

            # cria novo estado inicial que também é final com transição epsilon pro afn
            afn.add_estado(estado_inicial)
            afn.estado_inicial = estado_inicial
            afn.estados_finais.append(estado_inicial)

            afn.add_transicao(estado_inicial, afn1.estado_inicial, 'e')

            # itera pelo afn1 para adicionar os estados e transições no afn novo
            for k in afn1:
                afn.add_estado(k)

                # S1 ----A---> S2

            for i in range(len(list(afn1.values()))):
                for j in range(len(list(afn1.values())[i])):
                    afn.add_transicao(estado_inicial, list(afn1.values())[i][j][0], list(afn1.values())[i][j][1])
                    print(list(afn1.values())[i][j][0], 'i,j,0') # o estado em que vai a transição
                    print(list(afn1.values())[i][j][1], 'i,j,1') # o valor

            # for v in afn1[k][v]:
            #       afn.add_transicao(
            #          estado_inicial, afn1.estado_inicial, 'e')  # TODO
                    # afn.estados_finais.append(x) TODO adicionar os estados finais do afn1 no afn

            # afn.add_transicao(x, afn1.estado_inicial, 'e') TODO adicionar transição epsilon do estado final pro inicial

            pilha_afn.append(afn)
        elif pilha[i] == "+":
            pass
        elif pilha[i] == "|":
            afn2 = pilha_afn.pop()
            afn1 = pilha_afn.pop()
            afn = AFN()

            estado_inicial = 'S' + str(count)
            estado_final = 'S' + str(count+1)

            # adiciona novo estado inicial
            afn.add_estado(estado_inicial)
            afn.estado_inicial = estado_inicial

            # adiciona transições epsilon do novo estado inicial pros antigos estados inicias dos 2 afns
            afn.add_transicao(estado_inicial, afn1.estado_inicial, 'e')
            afn.add_transicao(estado_inicial, afn2.estado_inicial, 'e')

            # adiciona transição do novo afn pro afn1
            # TODO por o loop
            for i in range(len(list(afn1.values()))):
                for j in range(len(list(afn1.values())[i])):
                    # checar se é estado final antes
                    afn.add_transicao(estado_inicial, list(afn1.values())[i][j][0], list(afn1.values())[i][j][1])
                    print(list(afn1.values())[i][j][0], 'i,j,0') # o estado em que vai a transição
                    print(list(afn1.values())[i][j][1], 'i,j,1') # o valor
            
            afn.add_estado(afn1.estados_finais[0])
            afn.add_transicao(afn1.estado_inicial, afn1.estados_finais[0], list(
                afn1.keys())[1])  # list é o valor da transição

            # adiciona transição do novo afn pro afn2
            # TODO por o loop
            afn.add_estado(afn2.estados_finais[0])
            afn.add_transicao(afn2.estado_inicial, afn2.estados_finais[0], list(
                afn2.keys())[1])  # list é o valor da transição

            # cria um novo estado final e adiciona transições epsilon para ele
            afn.add_estado(estado_final)
            # TODO por o loop
            afn.add_transicao(afn1.estados_finais[0], estado_final, 'e')
            afn.add_transicao(afn2.estados_finais[0], estado_final, 'e')
            afn.estados_finais.append(estado_final)

            pilha_afn.append(afn)
        else:  # caso é uma letra do alfabeto
            simbolo = pilha[i]
            afn = AFN()
            estado_inicial = 'S' + str(count)
            estado_final = 'S' + str(count+1)

            afn.add_estado(estado_inicial)
            afn.estado_inicial = estado_inicial

            afn.add_transicao(estado_inicial, estado_final, simbolo)
            afn.estados_finais.append(estado_final)

            pilha_afn.append(afn)

        count = count + 1
        
    return pilha_afn[0]


# algoritmo_thompson("ab|*a.b.b.")

afn1 = AFN()

afn1.add_estado("S1")
afn1.add_estado("S2")
afn1.add_estado("S3")
afn1.add_estado("S4")

afn1.add_transicao("S1", "S2", "a")
afn1.add_transicao("S2", "S3", "b")
afn1.add_transicao("S3", "S4", "a")
afn1.add_transicao("S4", "S4", "a")

afn1.print_afn1()

# er = "(((a,b)+(a,e)+).)*"
