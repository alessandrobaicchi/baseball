import copy
import itertools
import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()        # E' un grafo semplice non diretto
        self._teams = []
        self._idMapTeams = None
        self._bestPath = []     # E' il percorso ottimo
        self._bestObjVal = 0    # E' il valore ottimo (somma dei pesi)


    # ======================================== Ricorsione ==============================================
    # E' fatta per _ricorsione()
    def getPath(self, v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]

        for v in self._grafo.neighbors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()


    # E' fatta per _ricorsioneV2()
    def getPathV2(self, v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]

        listaVicini = self.getVicini(parziale[-1])
        parziale.append(listaVicini[0][0])  # E' una navigazione su 2 livelli
        # listaVicini è una lista di tuple (vicino, peso)
        # listaVicini[0] prende la prima tupla (che ha il peso maggiore) nella lista di tuple (Liv 1)
        # listaVicini[0][0] sono dentro la tupla e prendo il suo primo elemento: vicino
        self._ricorsioneV2(parziale)

        return self._bestPath, self._bestObjVal

    # Ci sono 2 versioni di _ricorsione().

    # La prima è concettualmente corretta ma impossibile da testare
    # in tempi ragionevoli: impiegherebbe anni a dare risultati!

    # La seconda è "più rapida".

    # ------------------------------------ I versione --------------------------------------------
    # La funzione ricorsione fa le "solite" 3 cose:
    # 1) Verifica se la soluzione attuale è migliore della best (condizione di ottimalità);
    # 2) Verifica se ha senso uscire oppure no (condizione di terminazione);
    # 3) Verifica se può aggiungere qualcos'altro (ricorsione).
    def _ricorsione(self, parziale):
        print(len(parziale))

        # 1) Verifica se la soluzione attuale è migliore della best (condizione di ottimalità)
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        # 2) Verifica se ha senso uscire oppure no (condizione di terminazione)
        #    In realtà, qui non c'è una condizione di terminazione,
        #    perché nessuno mi dice "la tua soluzione deve essere lunga massimo tot".
        # --> la ricorsione termina solo quando non ci sono più nodi aggiungibili!

        # 3) Verifica se può aggiungere qualcos'altro (ricorsione)
        for v in self._grafo.neighbors(parziale[-1]):
            pesoE = self._grafo[parziale[-1]][v]["weight"]

            if self._grafo[parziale[-2]][parziale[-1]]["weight"] > pesoE and v not in parziale:
                # Se il peso dell'ultimo arco che inserito è maggiore del pesoE
                # e il vertice considerato v compare solo una volta,
                # allora vuol dire che il nodo v può essere inserito nella lista parziale.
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()
    # -----------------------------------------------------------------------------------------------

    # ---------------------------------- II versione ------------------------------------------------
        # La funzione ricorsione fa le "solite" 3 cose:
        # 1) Verifica se la soluzione attuale è migliore della best (condizione di ottimalità);
        # 2) Verifica se ha senso uscire oppure no (condizione di terminazione);
        # 3) Verifica se può aggiungere qualcos'altro (ricorsione).
    def _ricorsioneV2(self, parziale):

        # 1) Verifica se la soluzione attuale è migliore della best (condizione di ottimalità)
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        # 2) Verifica se ha senso uscire oppure no (condizione di terminazione)
        #    In realtà, qui non c'è una condizione di terminazione,
        #    perché nessuno mi dice "la tua soluzione deve essere lunga massimo tot".

        # 3) Verifica se può aggiungere qualcos'altro (ricorsione)
        # Prendo i vicini e li ordino per peso, e vado a prendere il primo in maniera tale da evitare di controllare,
        # per ogni layer della ricorsione, 29 vicini, ma controllarne solo 1.
        # Per far ciò sfrutto il metodo getVicini().

        listaVicini = self.getVicini(parziale[-1]) # (è una lista di tuple)
        # listaVicini è rispetto all'ultimo elemento aggiunto nella soluzione parziale.

        # Provo ad inserire il primo elemento di listaVicini che è raggiungibile.
        # Non è detto che possa aggiungere il primo elemento, perché l'arco potrebbe
        # avere un peso maggiore rispetto a quello che ho aggiunto fino a quel momento (quasi sempre sarà così).
        for v in listaVicini:
            if v[0] not in parziale and self._grafo[parziale[-2]][parziale[-1]]["weight"] > v[1]:
                # La seconda condizione dell'if significa:
                # "Il peso dell’ultimo arco inserito nel percorso deve essere maggiore del peso
                # del prossimo arco che voglio aggiungere".
                # Che è esattamente il vincolo del testo dell’esame:
                # “Il peso degli archi nel percorso deve essere strettamente decrescente.”
                # Dove: - parziale[-1] è l'ultimo nodo di parziale e parziale[-2] il penultimo nodo.
                #       - v è una tupla: v[0] è il nodo candidato e v[1] è il peso dell'arco tra
                #         parziale[-1] e v[0].
                parziale.append(v[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return
                # La chiave per rendere più efficiente questo metodo è la return.
                # Perché nel momento in cui ho trovato il miglior arco che posso aggiungere,
                # scorrendo da quello a peso maggiore a quello a peso minore,
                # evito di esplorare tutte le altre strade che hanno degli archi minori,
                # e questo mi permette di tagliare via tutta una serie di percorsi.

        # NOTA. In generale, non ci sono garanzie che questa _ricorsioneV2() permetta di trovare la soluzione ottima,
        # perché sto vincolando la ricerca in una certa direzione.
        # In questo caso, essendo un grafo completamente connesso in cui i pesi sono in qualche modo correlati ai nodi,
        # _ricorsioneV2() dovrebbe convergere alla soluzione ottima.
        # Però in generale, quando vincolo la procedura ricorsiva sto impedendo alla ricorsione di esplorare
        # un certo tipo di strade.
        # Quindi in linea di principio _ricorsioneV2() non è una soluzione globalmente ottima.
        # Sarebbe più corretta _ricorsione(), che però "dura anni".
    # -----------------------------------------------------------------------------------------------

    # Al metodo _score() arriva un lista di nodi. Sono sicuro che questi nodi sono connessi da archi,
    # perché li ho ottenuti da self._grafo.neighbors(v0).
    # Poi prende il peso e lo somma a score.
    def _score(self, parziale):
        score = 0
        for i in range(0, len(parziale)-1):
            score += self._grafo[parziale[i]][parziale[i+1]]["weight"]
        return score
    # ==================================================================================================




    def creaGrafo(self, year):
        self._grafo.clear()
        # In questo caso i nodi del grafo sono quelli contenuti nella lista self._teams, che
        # viene popolata in getTeamsOfYear()
        self._grafo.add_nodes_from(self._teams)

        # In questo caso, per gli archi non mi serve una query,
        # perché devo mettere un arco fra ogni possibile coppia di nodi: perché il GRAFO è COMPLETO.
        # Il modo più semplice per far ciò sono i seguenti.

        # Modo 1) Nota: mancano i pesi sugli archi
        # for u in self._grafo.nodes():
        #     for v in self._grafo.nodes():
        #         if u != v:
        #             self._grafo.add_edge(u, v)

        # Modo 2) Uso una funzione ad hoc della libreria itertools di Python
        # L’iteratore Combinations prende due argomenti: un interable (tipo una lista) e una quantità r,
        # e restituisce tutte le combinazioni degli elementi di quell’itertable r ad r
        myedges = list(itertools.combinations(self._teams, 2))
        # itertools.combinations() è un iteratore, devo metterlo in un lista. Poi passo questa lista
        # di tuple a self._grafo.add_edge(u,v): add_edge() vuole proprio liste di tuple!
        # In pratica sto prendendo i team due a due.
        self._grafo.add_edges_from(myedges)

        # A questo punto creo i pesi.
        # mapSalary è un dict in cui ho per ogni team il suo salario.
        mapSalary = DAO.getSalariesTeam(year, self._idMapTeams)
        # Ora per ogni arco del grafo calcolo il peso.
        for e in self._grafo.edges:
            # Ciclo sugli archi del grafo. Ogni arco è una tupla.
            # Il primo elemento è il nodo di partenza, il secondo elemento è il nodo di arrivo di quell'arco.
            # E uso il primo e il secondo elemento di questa tupla per accedere al dizionario mapSalary.
            salario1 = mapSalary[e[0]]
            salario2 = mapSalary[e[1]]
            peso = salario1 + salario2
            self._grafo[e[0]][e[1]]["weight"] = peso
            # Oppure in alternativa, faccio tutto in una riga.
            #self._grafo[e[0]][e[1]]["weight"] = mapSalary[e[0]] + mapSalary[e[1]]
        print("Test")


    # Il metodo getVicini() cerca tutti i vicini di source.
    # Essendo il grafo completamente connesso, vuol dire avere tutti i nodi del grafo, tranne source.
    # Poi, associa ad ognuno di questi vicini il peso che collega il source a tale nodo,
    # e infine ordina questa lista di nodi adiacenti a source.
    def getVicini(self, source):
        vicini = self._grafo.neighbors(source)
        # Costruisco una lista di tuple (viciniTuples) in cui il primo elemento è il vicino,
        # e il secondo elemento è il peso dell'arco che collega source al vicino.
        viciniTuples = []
        for v in vicini:
            viciniTuples.append((v, self._grafo[source][v]["weight"]))

        # Ordino viciniTuples per peso
        viciniTuples.sort(key=lambda x: x[1], reverse=True)

        return viciniTuples



    def getAllYears(self):
        return DAO.getAllYears()



    def getTeamsOfYear(self, year):
        self._teams = DAO.getTeamsOfYear(year)

        # Mi serve creare una idMapTeams
        self._idMapTeams = {t.ID: t for t in self._teams}
        # Ho scritto idMapTeams come dictionary comprehension.
        # Quindi mappo al t.ID l'oggetto t, per tutti gli oggetti contenuti nella lista self._teams.
        return self._teams



    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)


    # Funzione extra che prende a caso un nodo dalla lista dei _teams
    def getRandomNode(self):
        index = random.randint(0, len(self._teams))
        return self._teams[index]