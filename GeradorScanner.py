class Automato:
    def __init__(self):
        self.automato = {}
        self.estado_inicial = None
        self.estados_finais = []

        # é um dicionário no qual a chave é o vértice e os valores são listas de vértices
        # o vértice é um estado (e.g S1) e as listas de vértices são as transições (e.g S1->S2,S3)

    def add_estado(self, estado):
        if estado not in self.automato:
            self.automato[estado] = []

    def add_transicao(self, estado1, estado2, valor):
        self.automato[estado1].append((estado2, valor))


# ---------------- FUNÇÕES AUXILIARES ------------------- #

# checa se um automato tem transições vazias
def tem_transicoes_vazias(transicoes):
    vazio = False
    
    for j in range(len(transicoes)):
        if transicoes[j][1] == 'e':
            vazio = True
    
    return vazio

# percorre as transições de um automato para achar os estados que tem transições vazias
def achar_transicoes_vazias(transicoes):
    for j in range(len(transicoes)):
        if transicoes[j][1] == 'e':
            return transicoes[j][0]

# percorre o atne para calcular a árvore o valor do fecho
# dos estados que tem transição vazia
def percorrer_automato(estado, automato, visitados, res = ""):
    
    # a folha da árvore é se quando o estado não tem transições vazias
    # então o fecho e dele é ele mesmo
    if not tem_transicoes_vazias(automato.get(estado)):
        res = estado + "," + res
        return res

    # o estado_vazio é o estado em que o meu estado atual está indo com uma transição vazia
    estado_vazio = achar_transicoes_vazias(automato.get(estado))
    res = estado_vazio + "," + res 

    # checo item a item dentro da lista de estados em que meu estado atual vai
    # com transição vazia
    list_estados = estado_vazio.split(",")
    for item in list_estados:  
        # if para checar se o estado atual não está na transição da transição vazia dele
        # e.g. S1 --e--> S2 e S2 --e--> S1
        if item not in visitados:
            visitados = item + visitados
            res = percorrer_automato(item, automato, visitados, res)
        
    return res  


# ---------------------------- FUNÇÕES PRINCIPAIS ------------------------------ #

# ER -> AFNE
def algoritmo_thompson(er):
    pilha = list(er)
    pilha_afn = []
    count = 1

    for i in range(0, len(pilha)):
        if pilha[i] == '.':
            afn2 = pilha_afn.pop()
            afn1 = pilha_afn.pop()
            afn = Automato()

            # adiciona o estado inicial, vai ser sempre o estado inicial do afn mais a esquerda (o afn1)
            afn.estado_inicial = afn1.estado_inicial

            # adiciona todos estados e transições do afn1 pro novo afn
            for estado in afn1.automato:
                if estado in afn1.estados_finais:
                    afn.add_estado(estado)
                    # adiciona transição epsilon pro próximo afn
                    afn.add_transicao(estado, afn2.estado_inicial, 'e')
                for j in range(len(afn1.automato.get(estado))):
                    afn.add_estado(estado)
                    afn.add_transicao(estado, afn1.automato.get(estado)[
                                      j][0], afn1.automato.get(estado)[j][1])

            # adiciona todos estados e transições do afn2 pro novo afn
            for estado in afn2.automato:
                if estado in afn2.estados_finais:
                    # só copia o estado final
                    afn.add_estado(estado)
                    afn.estados_finais.append(estado)
                for j in range(len(afn2.automato.get(estado))):
                    afn.add_estado(estado)
                    afn.add_transicao(estado, afn2.automato.get(estado)[
                                      j][0], afn2.automato.get(estado)[j][1])

            pilha_afn.append(afn)
        elif pilha[i] == "*":
            afn1 = pilha_afn.pop()
            afn = Automato()

            estado_inicial = 'E' + str(count)

            # cria novo estado inicial que também é final com transição epsilon pro afn
            afn.add_estado(estado_inicial)
            afn.estado_inicial = estado_inicial
            afn.estados_finais.append(estado_inicial)
            afn.add_transicao(estado_inicial, afn1.estado_inicial, 'e')

            # adiciona todos estados e transições do afn1 (velho) pro novo afn
            for estado in afn1.automato:
                if estado in afn1.estados_finais:
                    afn.add_estado(estado)
                    # adiciona transição epsilon do estado final pro estado inicial
                    afn.add_transicao(estado, afn1.estado_inicial, 'e'),
                    afn.estados_finais.append(estado)
                for j in range(len(afn1.automato.get(estado))):
                    afn.add_estado(estado)
                    afn.add_transicao(estado, afn1.automato.get(estado)[
                                      j][0], afn1.automato.get(estado)[j][1])

            pilha_afn.append(afn)
        elif pilha[i] == "+":
            pass
        elif pilha[i] == "|":
            afn2 = pilha_afn.pop()
            afn1 = pilha_afn.pop()
            afn = Automato()

            estado_inicial = 'U' + str(count)
            estado_final = 'U' + str(count+1)

            # adiciona novo estado inicial
            afn.add_estado(estado_inicial)
            afn.estado_inicial = estado_inicial

            # adiciona transições epsilon do novo estado inicial pros antigos estados inicias dos 2 afns
            afn.add_transicao(estado_inicial, afn1.estado_inicial, 'e')
            afn.add_transicao(estado_inicial, afn2.estado_inicial, 'e')

            # adiciona todos estados e transições do afn1 pro novo afn
            for estado in afn1.automato:
                if estado in afn1.estados_finais:
                    afn.add_estado(estado)
                    afn.add_transicao(estado, estado_final, 'e')
                for j in range(len(afn1.automato.get(estado))):
                    afn.add_estado(estado)
                    afn.add_transicao(estado, afn1.automato.get(estado)[
                                      j][0], afn1.automato.get(estado)[j][1])

            # adiciona todos estados e transições do afn2 pro novo afn
            for estado in afn2.automato:
                if estado in afn2.estados_finais:
                    afn.add_estado(estado)
                    afn.add_transicao(estado, estado_final, 'e')
                for j in range(len(afn2.automato.get(estado))):
                    afn.add_estado(estado)
                    afn.add_transicao(estado, afn2.automato.get(estado)[
                                      j][0], afn2.automato.get(estado)[j][1])

            # adiciona o novo estado final
            afn.add_estado(estado_final)
            afn.estados_finais.append(estado_final)

            pilha_afn.append(afn)
        else:  # caso é uma letra do alfabeto
            simbolo = pilha[i]
            afn = Automato()
            estado_inicial = simbolo.upper() + str(count)
            estado_final = simbolo.upper() + str(count+1)

            afn.add_estado(estado_inicial)
            afn.estado_inicial = estado_inicial

            afn.add_transicao(estado_inicial, estado_final, simbolo)

            afn.add_estado(estado_final)
            afn.estados_finais.append(estado_final)

            pilha_afn.append(afn)

        count = count + 2

    return pilha_afn[0]

# AFNE -> AFN -> AFD
def construcao_subconjuntos(afne):
    pilha = []
    pilha.append(afne)
    afd = Automato()

    # (1) calcula o fecho epsilon #
    at_fecho = Automato()

    # copia o afne pro automato com fecho epsilon (at_fecho)
    for estado in afne.automato:
        if estado == afne.estado_inicial:
            at_fecho.add_estado(estado)
            at_fecho.estado_inicial = estado
        if estado in afne.estados_finais:
            at_fecho.add_estado(estado)
            at_fecho.estados_finais.append(estado)
        for j in range(len(afne.automato.get(estado))):
            at_fecho.add_estado(estado)
            at_fecho.add_transicao(estado, afne.automato.get(estado)[
                j][0], afne.automato.get(estado)[j][1])
    
    res_fecho = None

    # adiciona fecho epsilon no at_fecho TODO
    for estado in afne.automato:
        if tem_transicoes_vazias(afne.automato.get(estado)):
            res = percorrer_automato(estado,afne.automato,estado)
            res = res + estado
            
            # para arrumar a resposta da função que calcula os fechos
            # 1- converto para set para remover repetidos (usando as vírgulas como separador)
            # 2- converto para lista e removo espaços em branco
            # 3- converto pra string colocando vírgulas de novo para separar os estados
            fecho_e = list(set(res.split(',')))
            # fecho_e.remove("")
            fecho_e = ",".join(fecho_e)

            at_fecho.add_transicao(estado, fecho_e, 'fecho (e)')
        else:
            at_fecho.add_transicao(estado, estado, 'fecho (e)')
                
    # remove todas as transições 'e' do at_fecho TODO
                
    # (2) converte afne para afn #
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

    # (3) converte afn para afd # TODO

    return at_fecho

# meu_novo_afn = algoritmo_thompson("ab|*a.")
# print(meu_novo_afn.automato)
# print(meu_novo_afn.estado_inicial)
# print(meu_novo_afn.estados_finais)

# er = "(((a,b)+(a,e)+).)*"

afne = Automato()
afne.estado_inicial = 'S1'
afne.estados_finais.append('S3')
afne.automato = {'S1': [('S2', 'a'), ('S4,S2', 'e')],
                 'S2': [('S3', 'a'), ('S1,S3', 'e')],
                 'S3': [('S3', 'a')],
                 'S4': [('S4', 'a')]}

res = construcao_subconjuntos(afne)

print(res.automato, 'fim')