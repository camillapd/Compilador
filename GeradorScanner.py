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
        if (estado2 != "" and valor != "") and (estado1 in self.automato and (estado2, valor) not in self.automato.get(estado1)):
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
    transicoes_vazias = ""

    for j in range(len(transicoes)):
        if transicoes[j][1] == 'e':
            transicoes_vazias = transicoes[j][0] + ',' + transicoes_vazias

    return transicoes_vazias


# percorre o atne para calcular a árvore o valor do fecho
# dos estados que tem transição vazia
def percorrer_automato(estado, automato, visitados, res=""):

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


# parar renomear o estado final do automato
def renomeia_estado_final(nome, afn_velho):
    afn = Automato()
    afn.add_estado(nome)
    afn.estados_finais.append(nome)

    # (1) copia o automato antigo para o novo
    for estado in afn_velho.automato:
        if estado == afn_velho.estado_inicial:
            afn.estado_inicial = estado
        for j in range(len(afn_velho.automato.get(estado))):
            estado_destino = afn_velho.automato.get(estado)[j][0]
            # (1a) para checar se o estado em que tenho transição é o antigo estado final e vai nele mesmo
            # mantenho o símbolo e mudo o resto
            if estado in afn_velho.estados_finais:
                if estado_destino in afn_velho.estados_finais:
                    afn.add_transicao(
                        nome, nome, afn_velho.automato.get(estado)[j][1])
                # se for transição para outro estado eu só mudo o estado origem
                else:
                    afn.add_transicao(nome, estado_destino,
                                      afn_velho.automato.get(estado)[j][1])
            else:
                afn.add_estado(estado)
                # (1b) aqui checo se for transição de um estado comum para o estado final antigo e mudo para o novo
                if estado_destino in afn_velho.estados_finais:
                    afn.add_transicao(
                        estado, nome, afn_velho.automato.get(estado)[j][1])
                else:
                    afn.add_transicao(estado, estado_destino,
                                      afn_velho.automato.get(estado)[j][1])

    return afn


# ---------------------------- FUNÇÕES PRINCIPAIS ------------------------------ #

# ER -> AFNE
def algoritmo_thompson(pilha, nome):
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
                    if estado != afn2.estado_inicial:
                        afn.estados_finais.append(estado)
                for j in range(len(afn2.automato.get(estado))):
                    afn.add_estado(estado)
                    afn.add_transicao(estado, afn2.automato.get(estado)[
                                      j][0], afn2.automato.get(estado)[j][1])

            pilha_afn.append(afn)
        elif pilha[i] == "*":
            afn1 = pilha_afn.pop()
            afn = Automato()

            estado_inicial = 'S' + str(count)

            # cria novo estado inicial que também é final com transição epsilon pro afn
            afn.add_estado(estado_inicial)
            afn.estado_inicial = estado_inicial
            afn.estados_finais.append(estado_inicial)
            afn.add_transicao(estado_inicial, afn1.estado_inicial, 'e')

            # adiciona todos estados e transições do afn1 (velho) pro novo afn
            for estado in afn1.automato:
                if estado in afn1.estados_finais:
                    afn.add_estado(estado)
                    # adiciona transição epsilon do estado final pro estado inicial antigo
                    afn.add_transicao(estado, afn1.estado_inicial, 'e'),
                    afn.estados_finais.append(estado)
                for j in range(len(afn1.automato.get(estado))):
                    afn.add_estado(estado)
                    afn.add_transicao(estado, afn1.automato.get(estado)[
                                      j][0], afn1.automato.get(estado)[j][1])

            pilha_afn.append(afn)
        elif pilha[i] == "+":
            afn1 = pilha_afn.pop()
            afn = Automato()

            estado_inicial = 'S' + str(count)

            # cria novo estado inicial que também é final com transição epsilon pro afn
            afn.add_estado(estado_inicial)
            afn.estado_inicial = estado_inicial
            afn.estados_finais.append(estado_inicial)
            afn.add_transicao(estado_inicial, afn1.estado_inicial, 'e')

            # adiciona todos estados e transições do afn1 (velho) pro novo afn
            for estado in afn1.automato:
                if estado in afn1.estados_finais:
                    afn.add_estado(estado)
                    # adiciona transição epsilon do estado final pro estado inicial novo
                    afn.add_transicao(estado, afn.estado_inicial, 'e'),
                    afn.estados_finais.append(estado)
                for j in range(len(afn1.automato.get(estado))):
                    afn.add_estado(estado)
                    afn.add_transicao(estado, afn1.automato.get(estado)[
                                      j][0], afn1.automato.get(estado)[j][1])

            pilha_afn.append(afn)
        elif pilha[i] == "|":
            afn2 = pilha_afn.pop()
            afn1 = pilha_afn.pop()
            afn = Automato()

            estado_inicial = 'S' + str(count)
            estado_final = 'S' + str(count+1)

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
        elif pilha[i] == "?":
            afn1 = pilha_afn.pop()
            afn = Automato()
            afn.estado_inicial = afn1.estado_inicial

            for estado in afn1.automato:
                if estado in afn1.estados_finais:
                    afn.estados_finais.append(estado)
                for j in range(len(afn1.automato.get(estado))):
                    afn.add_estado(estado)
                    afn.add_transicao(estado, afn1.automato.get(estado)[
                                      j][0], afn1.automato.get(estado)[j][1])

            # adiciona transições vazias do estado inicial direto para o final
            for i in len(afn.estados_finais):
                afn.add_transicao(afn.estado_inicial,
                                  afn.estados_finais[i], "e")

            pilha_afn.append(afn)
        else:  # caso é uma letra do alfabeto
            if pilha[i] == "\\":
                simbolo = pilha[i+1]
            else:
                simbolo = pilha[i]

            afn = Automato()
            estado_inicial = "S" + str(count)
            estado_final = "S" + str(count+1)
            afn.add_estado(estado_inicial)
            afn.estado_inicial = estado_inicial

            afn.add_transicao(estado_inicial, estado_final, simbolo)

            afn.add_estado(estado_final)
            afn.estados_finais.append(estado_final)

            pilha_afn.append(afn)

        count = count + 2

    # Para renomear o estado final no meu afn para o nome do token #
    afn = renomeia_estado_final(nome, pilha_afn[0])

    return afn


# AFNE -> Automato com fecho (e) - as transições vazias -> AFN
def construcao_subconjuntos(afne):
    lista_simbolos = []

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

    # adiciona fecho epsilon no at_fecho
    for estado in afne.automato:
        if tem_transicoes_vazias(afne.automato.get(estado)):
            res = percorrer_automato(estado, afne.automato, estado)
            res = res + estado

            # para arrumar a resposta da função que calcula os fechos
            # 1- converto para set para remover repetidos (usando as vírgulas como separador)
            # 2- converto para lista e removo espaços em branco
            # 3- converto pra string colocando vírgulas de novo para separar os estados
            fecho_e = list(set(res.split(',')))
            fecho_e.remove("")
            fecho_e = ",".join(fecho_e)

            at_fecho.add_transicao(estado, fecho_e, 'fecho (e)')
        else:
            at_fecho.add_transicao(estado, estado, 'fecho (e)')

    # (2) converte afne para afn #
    afn = Automato()

    # crio uma lista com símbolos não vazios de transições no meu automato com fecho
    for estado in at_fecho.automato:
        for j in range(len(at_fecho.automato.get(estado))-1):
            if at_fecho.automato.get(estado)[j][1] != 'e' and at_fecho.automato.get(estado)[j][1] not in lista_simbolos:
                lista_simbolos.append(at_fecho.automato.get(estado)[j][1])

    for estado in at_fecho.automato:
        # o valor do fecho do estado atual
        fecho_estado = at_fecho.automato.get(estado)[-1][0]
        afn.add_estado(estado)
        # (2a) adiciono todos os estados do at_fecho no afn novo #
        if estado == at_fecho.estado_inicial:
            # mudar para lista se der problemas depois *lembrete* #
            afn.estado_inicial = fecho_estado
        if estado in at_fecho.estados_finais:
            afn.estados_finais.append(estado)

        # o símbolo da setinha que vou colocar para o novo estado do afn
        fecho_res = ""
        simbolo_res = ""

        for simbolo in lista_simbolos:  # possivelmente gambiarra
            # (2b) eu preciso olhar para o valor do fecho na transição atual #
            # e.g: S1 --a--> S2 e fecho (e) S1 = {S1,S2,S3,S4} :: eu pego o segundo valor
            # então checo se esse valor é uma lista de estados se for eu coloco os valores em uma lista e itero por eles
            if "," in fecho_estado:
                list_fecho = fecho_estado.split(",")
                for fecho in list_fecho:
                    # aqui eu checo se tem mais de uma transição nesse estado
                    # porque se tiver uma só é o fecho e não quero contar isso nas minhas setinhas
                    for j in range(len(at_fecho.automato.get(fecho))-1):
                        if len(at_fecho.automato.get(fecho)) > 1 and at_fecho.automato.get(fecho)[j][1] == simbolo:
                            # (2c) agora com o valor do fecho, eu salvo o estado em que ele vai com a transição que quero #
                            # (2d) com o estado destino eu pego o fecho deste estado #
                            simbolo_res = simbolo
                            estado_destino = at_fecho.automato.get(fecho)[j][0]
                            fecho_destino = at_fecho.automato.get(
                                estado_destino)[-1][0]

                            # checagem para não colocar valores repetidos na transição nova
                            if fecho_destino not in fecho_res:
                                # como tem mais de um estado em que estou olhando o fecho, aqui junto todos
                                fecho_res = fecho_destino + ',' + fecho_res

                # (2e) aqui adiciono a transição, que vai do meu estado para os fechos desse estado,
                # e vejo qual o estado transição deles e pego o fecho #
                # para remover a última vírgula
                if fecho_res != "" and fecho_res[-1] == ",":
                    fecho_res = fecho_res[:-1]
                afn.add_transicao(estado, fecho_res, simbolo_res)
                fecho_res = ""
            else:
                # aqui eu checo se tem mais de uma transição nesse estado
                # porque se tiver uma só é o fecho e não quero contar isso nas minhas setinhas
                for j in range(len(at_fecho.automato.get(fecho_estado))-1):
                    if len(at_fecho.automato.get(fecho_estado)) > 1 and at_fecho.automato.get(fecho_estado)[0][1] == simbolo:
                        # mesmo que (2c) e (2d)
                        simbolo_res = simbolo
                        estado_destino = at_fecho.automato.get(fecho_estado)[
                            0][0]
                        fecho_res = at_fecho.automato.get(
                            estado_destino)[-1][0]

                # (2f) aqui adiciono a transição (segundo caso)
                if fecho_res != "" and fecho_res[-1] == ",":
                    fecho_res = fecho_res[:-1]
                afn.add_transicao(estado, fecho_res, simbolo_res)

    return afn


# AFN -> AFD
def conversao_afd(afn, nome):
    afd = Automato()
    cria_afd = True
    # aqui eu crio uma pilha em que vai ter os estados novos do afd
    pilha = []
    count = 0

    # 1 - o novo estado inicial são os estados inicias anteriores #
    afd.add_estado(afn.estado_inicial)
    afd.estado_inicial = afn.estado_inicial
    estado_destino = afn.estado_inicial
    pilha.append(afn.estado_inicial)

    # no loop eu adiciono os estados e transições conforme vão aparecendo
    # nas transições do estado inicial e estados consequentes
    # o loop só termina quando novos estados de transição já estão nos estados do afd

    # 2 - loop em que adiciono os estados e transições do afd #
    while cria_afd:
        estado_res = {}
        # na pilha eu removo os estados e faço minha conversão
        # eu pego de uma pilha porque no caso de eu adicionar dois estados de uma vez no afd
        # nenhum estado vai ser esquecido
        estado = pilha.pop()
        count = 0

        if "," not in estado:
            for j in range(len(afn.automato.get(estado))):
                # aqui eu pego o estado da transição (no afn) do estado atual do afd e o símbolo de transição
                estado_destino = afn.automato.get(estado)[j][0]
                simbolo = afn.automato.get(estado)[j][1]
                # eu adiciono a transição
                afd.add_transicao(estado, estado_destino, simbolo)
                # adiciono o estado novo somente se ele tem transições ou se é um estado final
                # e se já não coloquei ele no afd
                if (estado_destino in afn.estados_finais or len(afn.automato.get(estado_destino)) > 0) and estado_destino not in afd.automato:
                    afd.add_estado(estado_destino)
                    pilha.append(estado_destino)
                elif len(afn.automato.get(estado_destino)) == 0:
                    pass
        else:
            list_estados = estado.split(",")
            for item in list_estados:
                for j in range(len(afn.automato.get(item))):  # TODO
                    # aqui eu uso um dicionário para acumular os valores das transições dos estados em que estou iterando
                    # porque preciso acumular os estados de destino, mas manter o mesmo símbolo
                    estado_destino = afn.automato.get(item)[j][0]
                    simbolo = afn.automato.get(item)[j][1]

                    if simbolo in estado_res:
                        estado_res[simbolo] = estado_res[simbolo] + \
                            ',' + estado_destino
                    else:
                        estado_res[simbolo] = estado_destino
                    # existe um problema aqui
                    # provavelmente em todas as partes em que tem mais de um símbolo de transição (e.g: a,b,c em vez de só a)
                    # consertado aqui TODO checar nas outras partes
            if len(estado_res) != 0:
                for simbolo in estado_res:
                    res = list(set(estado_res.get(simbolo).split(',')))
                    res = ",".join(res)
                    if res not in afd.automato:
                        afd.add_estado(res)
                        pilha.append(res)
                    afd.add_transicao(estado, res, simbolo)

        # percorro todo o meu afd
        # para cada estado em que: tenho transições nele or ele é estado final eu aumento +1
        for estado2 in afd.automato:
            if len(afd.automato.get(estado2)) > 0 or estado2 in afn.estados_finais:
                count = count + 1

        # então nesse if eu checo se o contador tem o mesmo valor do comprimento do afd
        # ou seja, se todos os meus estados nele tem transições (ou é um estado final)
        # o que significa que terminei de converter o afn para afd
        if count == len(afd.automato):
            cria_afd = False

    # 3 - adiciono estados finais #
    # um estado não determistico é final se um dos estados que compõe ele era final no afn
    for estado in afd.automato:
        if "," not in estado:
            if estado in afn.estados_finais and estado not in afd.estados_finais:
                afd.estados_finais.append(estado)
        else:
            list_estados = estado.split(",")
            for item in list_estados:
                if item in afn.estados_finais and estado not in afd.estados_finais:
                    afd.estados_finais.append(estado)

    # 4 - renomeio os meus estados #
    afd_novo = renomeia_estado_final(nome, afd)

    return afd_novo


# er = "(((a,b)+(a,c)+).)*"
# er2 = "ab|*a." = (a|b)*.a
# er3 = "ab|*a.b.b."

er1 = ["LET", "DATA", "|", "READ", "|", "RESTORE", "|", "DIM", "|",
       "IF", "|", "THEN", "|", "ELSE", "|",
       "FOR", "|", "TO", "|", "STEP", "|", "NEXT", "|",
       "WHILE", "|", "WEND", "|", "REPEAT", "|", "UNTIL", "|",
       "DO", "|", "LOOP", "|", "UNTIL", "|",
       "GOTO", "|", "GOSUB", "|", "RETURN", "|", "ON", "|",
       "LIST", "|", "PRINT", "|", "INPUT", "|", "TAB", "|", "SPC", "|",
       "ABS", "|", "ATN", "|", "COS", "|", "EXP", "|", "INT", "|", "LOG", "|", "RAND", "|", "SIN", "|", "SQR", "|", "TAN", "|",
       "REM", "|", "USR", "|", "CALL", "|", "TRON", "|", "ASM", "|"]
token1 = "keywords"

er2 = ["A", "B", "|", "C", "|", "D", "|", "E", "|", "F", "|", "G", "|", "H", "|", "I", "|", "J", "|",
       "K", "|", "L", "|", "M", "|", "N", "|", "O", "|", "P", "|", "Q", "|",
       "R", "|", "S", "|", "T", "|", "U", "|", "V", "|", "W", "|", "X", "|", "Y", "|", "Z", "|",
       "0", "|", "1", "|", "2", "|", "3", "|", "4", "|", "5", "|", "6", "|", "7", "|", "8", "|", "9", "|", "?", "."]
token2 = "ID"

er3 = ["<>", ">=", "|", "<=", "|", "\\+", "|", "-", "|", "\\*", "|", "/", "|",]
token3 = "operators"

er4 = ["0", "1", "|", "2", "|", "3", "|", "4", "|", "5", "|", "6", "|", "7", "|", "8", "|", "9", "|", "\\.",
       "0", "1", "|", "2", "|", "3", "|", "4", "|", "5", "|", "6", "|", "7", "|", "8", "|", "9", "|", "+", "."]
token4 = "number"

res = algoritmo_thompson(er1, token1)
print(res.automato, '\n ~~~~ AFNE')
print(res.estado_inicial, 'inicial')
print(res.estados_finais, 'finais \n')

res2 = construcao_subconjuntos(res)
print(res2.automato, '\n ~~~~ AFN')
print(res2.estado_inicial, 'inicial')
print(res2.estados_finais, 'finais \n')

res3 = conversao_afd(res2, token1)
print(res3.automato, 'afd')
print(res3.estado_inicial, 'inicial')
print(res3.estados_finais, 'finais')
