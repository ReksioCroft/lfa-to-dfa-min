import queue


def lfa_to_nfa(lfa):
    def dfs(Nod):
        v.append(Nod)
        for i in lfa[2][Nod]["$"]:
            if i not in v:
                dfs(i)

    # 1.1 Calculam inchiderea la lambda
    lClosure = []
    for nod in range(automat[0]):
        v = []
        dfs(nod)
        lClosure.append(v)
    # print(lClosure)

    # 1.2 Calculam functia de tranzitie
    alfabet = automat[1]
    alfabet.pop(alfabet.index("$"))
    # print(alfabet)
    tranzition = {i: [] for i in alfabet}
    for ch in alfabet:
        #  print()
        for i in range(automat[0]):
            v = []
            for j in lClosure[i]:
                for nod in automat[2][j][ch]:
                    if nod not in v:
                        v.append(nod)
            ls = []
            for j in v:
                for nod in lClosure[j]:
                    if nod not in ls:
                        ls.append(nod)
            # print(sorted(ls))
            tranzition[ch].append(sorted(ls))

    # print(tranzition)
    # Pasul 1.3: Calculam starile finale
    finale = []
    for i in range(automat[0]):
        for j in lClosure[i]:
            if j in automat[4]:
                finale.append(i)
                break
    # print(finale)
    # Pasul 1.4: Eliminarea starilor redundante
    inlocuire = {i: i for i in range(automat[0])}
    for i in range(automat[0]):
        for j in range(i + 1, automat[0]):
            if (i in finale) == (j in finale):
                for ch in alfabet:
                    if tranzition[ch][i] != tranzition[ch][j]:
                        break
                else:  # daca functia de tranzitie e aceeasi pt toate literele din alfabet
                    inlocuire[j] = inlocuire[i]
    # print(inlocuire)
    # returnam automatul si renumerotam stariile
    Q = []
    # print(tranzition)
    co = 0
    renumerotare = []
    for i in range(automat[0]):
        if inlocuire[i] != i:
            co += 1
        renumerotare.append(co)

    for i in range(automat[0]):
        if inlocuire[i] == i:
            Q.append({j: [] for j in alfabet})
            for j in alfabet:
                for k in tranzition[j][i]:
                    if inlocuire[k] not in Q[-1][j]:
                        Q[-1][j].append(inlocuire[k] - renumerotare[inlocuire[k]])
    # print(Q)
    # recalculam starile finale dupa eliminare noduri si renumerotare
    for i in finale:
        if inlocuire[i] != i:
            finale.pop(finale.index(i))
    for i in range(len(finale)):
        finale[i] = finale[i] - renumerotare[finale[i]]
    return [automat[0] - renumerotare[automat[0] - 1], alfabet, Q, automat[3] - renumerotare[automat[3]], finale]


def nfa_to_dfa(automat):
    # Am ales sa nu pastrez numaratoare initiala a nodurilor
    q = queue.Queue()
    q.put([automat[3]])
    Q = [{i: [] for i in automat[1]}]
    # vizitat = [automat[3]]
    denumiri = {tuple([automat[3]]): 0}
    while q.empty() == False:
        nod0 = q.get()
        for ch in automat[1]:
            ls = []
            for nod in nod0:
                for i in automat[2][nod][ch]:
                    if i not in ls:
                        ls.append(i)
            if len(ls) > 0:
                if tuple(ls) not in denumiri:  # inseamna ca nu l-am vizitat, deci ii dam un nume si il bagam in coada
                    denumiri[tuple(ls)] = len(denumiri)
                    for i in range(len(Q), len(denumiri)):  # ma asigur sa aloc suicient spatiu pt noile noduri
                        Q.append({j: [] for j in automat[1]})
                    q.put(ls)
                Q[denumiri[tuple(nod0)]][ch].append(denumiri[tuple(ls)])

    # calculare stari finale
    finale = []
    for i in denumiri:
        for j in i:
            if j in automat[4]:
                finale.append(denumiri[i])
                break
    if "$" in automat[1]:
        automat[1].pop(automat[1].index("$"))
    return [len(denumiri), automat[1], Q, 0, finale]


def min_dfa(automat):
    echiv = [[True for j in range(i)] for i in range(automat[0])]
    # print(echiv)
    for i in range(automat[0]):
        for j in range(i):
            if ( i in automat[4] ) != ( j in automat[4] ):
                echiv[i][j] = False
    ok = True
    print(automat[2])
    while ok == True:
        ok = False
        for i in range(automat[0]):
            for j in range(i):
                for ch in automat[1]:
                    i1 = automat[2][i][ch][0]
                    j1 = automat[2][j][ch][0]
                    if echiv[i][j] == True and (
                            (i1 > j1 and echiv[i1][j1] == False) or (j1 > i1 and echiv[j1][i1] == False)):
                        echiv[i][j] = False
                        ok = True

    print(echiv)
    return


fin = open("automat.in")
nrStari = int(fin.readline())
fin.readline()
alfabet = fin.readline().split()
if "$" not in alfabet:
    alfabet.append("$")
stare0 = int(fin.readline())
fin.readline()
finale = [int(x) for x in fin.readline().split()]
fin.readline()
Q = [{j: [] for j in alfabet} for i in range(nrStari)]
for i in fin:
    ls = i.split()
    a = int(ls[0])
    b = int(ls[2])
    ch = ls[1]
    ls = Q[a][ch]
    ls.append(b)
    Q[a][ch] = ls
fin.close()

automat = [nrStari, alfabet, Q, stare0, finale]

# print(automat)
# automat = lfa_to_nfa(automat)
print(automat)
automat = nfa_to_dfa(automat)
print(automat)
automat = min_dfa(automat)
print(automat)
