from database.DAO import DAO
from model.model import Model

listObjects = DAO.getAllNodes()
print(len(listObjects))

mymodel = Model()
mymodel.buildGraph()
edges = DAO.getAllArchi(mymodel.getIdMap())

print(len(edges))