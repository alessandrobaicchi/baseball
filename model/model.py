import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()        # E' un grafo semplice non diretto
        self._teams = []


    def creaGrafo(self):
        # In questo caso i nodi del grafo sono quelli contenuti nella lista self._teams, che
        # viene popolata in getTeamsOfYear()
        self._grafo.add_nodes_from(self._teams)


    def getAllYears(self):
        return DAO.getAllYears()


    def getTeamsOfYear(self, year):
        self._teams = DAO.getTeamsOfYear(year)
        return self._teams