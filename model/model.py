import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()        # E' un grafo semplice non diretto
        self._teams = []
        self._idMapTeams = None


    # ======================================== Ricorsione ==============================================
    def getPath(self):
        pass


    def _ricosione(self):
        pass








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