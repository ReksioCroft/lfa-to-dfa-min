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
    tranzition = {i:[] for i in alfabet if i != '$'}
    for ch in automat[1]:
      #  print()
        if ch != "$":
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

    print(tranzition)
    return


fin = open("automat.in")
nrStari = int(fin.readline())
fin.readline()
alfabet = fin.readline().split()
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

automat = lfa_to_nfa(automat)
