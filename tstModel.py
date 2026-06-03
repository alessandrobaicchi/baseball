from model.model import Model

mymodel = Model()
mymodel.getTeamsOfYear(2012)
mymodel.creaGrafo(2012)
nodi, archi = mymodel.getGraphDetails()
print(f"Grafo creato! Il grafo contiente {nodi} nodi e {archi} archi.")
