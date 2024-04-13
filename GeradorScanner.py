class AFN:
    def __init__(self):
        self.meu_afn = {}
        self.estado_inicial = None
        self.estados_finais = []

        # o afn é um meu_afn
        # é um dicionário no qual a chave é o vértice e os valores são listas de vértices
        # o vértice é um estado (e.g S1) e as listas de vértices são as transições (e.g S1->S2,S3)

    def add_estado(self, estado):
        if estado not in self.meu_afn:
            self.meu_afn[estado] = []

    def add_transicao(self, estado1, estado2, valor):
        self.meu_afn[estado1].append((estado2, valor))

def algoritmo_thompson(er):
    pilha = list(er)
    pilha_afn = []
    count = 1

    for i in range(0, len(pilha)):
        if pilha[i] == '.':
            afn2 = pilha_afn.pop()
            afn1 = pilha_afn.pop()
            afn = AFN()

            # adiciona o estado inicial, vai ser sempre o estado inicial do afn mais a esquerda (o afn1)
            afn.estado_inicial = afn1.estado_inicial

            # adiciona todos estados e transições do afn1 pro novo afn                    
            for i in afn1.meu_afn:
                estado = i
                if estado in afn1.estados_finais:
                    afn.add_estado(estado)
                    # adiciona transição epsilon pro próximo afn
                    afn.add_transicao(estado, afn2.estado_inicial, 'e')
                for j in range(len(afn1.meu_afn.get(estado))):
                    afn.add_estado(estado)
                    afn.add_transicao(estado, afn1.meu_afn.get(estado)[
                                      j][0], afn1.meu_afn.get(estado)[j][1])                

            # adiciona todos estados e transições do afn2 pro novo afn          
            for i in afn2.meu_afn:
                estado = i
                if estado in afn2.estados_finais:
                    # só copia o estado final
                    afn.add_estado(estado)
                    afn.estados_finais.append(estado)
                for j in range(len(afn2.meu_afn.get(estado))):
                    afn.add_estado(estado)
                    afn.add_transicao(estado, afn2.meu_afn.get(estado)[
                                      j][0], afn2.meu_afn.get(estado)[j][1])

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

            # adiciona todos estados e transições do afn1 (velho) pro novo afn
            for i in afn1.meu_afn:
                estado = i
                if estado in afn1.estados_finais:
                    afn.add_estado(estado)
                    # adiciona transição epsilon do estado final pro estado inicial
                    afn.add_transicao(estado, afn1.estado_inicial, 'e'),
                    afn.estados_finais.append(estado)
                for j in range(len(afn1.meu_afn.get(estado))):

                    afn.add_estado(estado)
                    afn.add_transicao(estado, afn1.meu_afn.get(estado)[
                                      j][0], afn1.meu_afn.get(estado)[j][1])

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
            
            # adiciona todos estados e transições do afn1 pro novo afn
            for i in afn1.meu_afn:
                estado = i
                if estado in afn1.estados_finais:
                    afn.add_estado(estado)
                    afn.add_transicao(estado, estado_final, 'e')
                for j in range(len(afn1.meu_afn.get(estado))):
                    afn.add_estado(estado)
                    afn.add_transicao(estado, afn1.meu_afn.get(estado)[
                                      j][0], afn1.meu_afn.get(estado)[j][1])
                             
            # adiciona todos estados e transições do afn2 pro novo afn          
            for i in afn2.meu_afn:
                estado = i
                if estado in afn2.estados_finais:
                    afn.add_estado(estado)
                    afn.add_transicao(estado, estado_final, 'e')
                for j in range(len(afn2.meu_afn.get(estado))):
                    afn.add_estado(estado)
                    afn.add_transicao(estado, afn2.meu_afn.get(estado)[
                                      j][0], afn2.meu_afn.get(estado)[j][1])

            # adiciona o novo estado final
            afn.add_estado(estado_final)
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

            afn.add_estado(estado_final)
            afn.estados_finais.append(estado_final)

            pilha_afn.append(afn)

        count = count + 2

    return pilha_afn[0]

meu_novo_afn = algoritmo_thompson("ab|*a.b.")
print(meu_novo_afn.meu_afn)
print(meu_novo_afn.estado_inicial)
print(meu_novo_afn.estados_finais)

# er = "(((a,b)+(a,e)+).)*"
