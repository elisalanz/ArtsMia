import copy

import networkx as nx
from networkx.classes import neighbors

from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMap = {}
        for v in self._nodes:
            self._idMap[v.object_id] = v
        self._bestPath = []
        self._bestCost = 0

    def buildGraph(self):
        nodes = DAO.getAllNodes()
        self._graph.add_nodes_from(nodes)
        self.addAllEdges()

    def addEdgesV1(self):
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getPeso(u, v)
                if peso != None:
                    self._graph.add_edge(u, v, weight = peso)

    def addAllEdges(self):
        allEdges = DAO.getAllArchi(self._idMap)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)


    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getIdMap(self):
        return self._idMap

    def getInfoConnessa(self, idInput):
        """
        Identifica la componente connessa che contiene idInput e ne rstituisce la dimensione
        """
        # if self.hasNode(idInput):
        #     return None
        # controllo ridondante

        source = self._idMap[idInput]

        # MODO 1: conto i successori
        succ = nx.dfs_successors(self._graph, source).values()
        # posso avere delle liste di successori
        res = []
        for s in succ:
            res.extend(s)
        # per contare tutti gli elementi
        print("Size connessa con modo 1:", len(res))

        # MODO 2: conto i predecessori
        pred = nx.dfs_predecessors(self._graph, source)
        print("Size connessa con modo 2:", len(pred.values()))

        # MODO 3: conto i  nodi dell'albero di visita
        dfsTree = nx.dfs_tree(self._graph, source)
        print("Size connessa con modo 3:", len(dfsTree.nodes()))

        # MODO 4: uso il metodo nodes_connected_component di networkx
        conn = nx.node_connected_component(self._graph, source)
        print("Size connessa con modo 4:", len(conn))

        return len(conn)

    def hasNode(self, idInput):
        return idInput in self._idMap # se è true, allora c'è anche nel grafo

    def getObjectFromId(self, id):
        return self._idMap[id]

    def getOptPath(self, source, lun):
        self._bestPath = []
        self._bestCost = 0

        parziale = [source]

        for n in nx.neighbors(self._graph, source):  # self._graph.neighbors(source)
            if parziale[-1].classification == n.classification and n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()

        return self._bestPath, self._bestCost

    def _ricorsione(self, parziale, lun):
        if len(parziale) == lun:
            # allora parziale ha la lunghezza desiderata, verifico se è una soluzione migliore e in ogni caso esco
            if self.costo(parziale) > self._bestCost:
                self._bestCost = self.costo(parziale)
                self._bestPath = copy.deepcopy(parziale) # per evitare il riferimento a parziale (che nel mentre cambierà)
            return

        # se arrivo qui, allora parziale può ancora ammettere altri nodi
        for n in self._graph.neighbors(parziale[-1]):
            if parziale[-1].classification == n.classification and n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()

    def costo(self, listObjects):
        totCosto = 0
        for i in range(0, len(listObjects)-1):  # ciclo sugli archi, non sui nodi
            totCosto += self._graph[listObjects[i]][listObjects[i+1]]['weight']
        return totCosto