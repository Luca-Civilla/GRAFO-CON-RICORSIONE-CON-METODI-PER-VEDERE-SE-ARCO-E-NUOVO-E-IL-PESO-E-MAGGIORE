import copy
import geopy

from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self._colori = DAO.get_all_colors()
        self._grafo = nx.Graph()
        self._idProducts_Map = {}
        self._prodotti = []
        self._listaBest = []
        #self.lista_prodotti = []
        #RICORSIONE
        self._solBest = []
        self._pesoArco = 0

    # def cercaPercorso(self,v0):
    #     self._solBest = []
    #     self._pesoArco = 0
    #     punto = self._idProducts_Map[v0]
    #     parziale = [punto]
    #     self._ricorsione(parziale)
    #
    #     return self._solBest
    #
    # def _ricorsione(self, parziale):
    #
    #     if len(parziale)>len(self._solBest):
    #         self._solBest = copy.deepcopy(parziale)
    #
    #
    #     vicini = self._grafo.neighbors(parziale[-1])
    #     for v in vicini:
    #         if v not in parziale:
    #             pesoEdge = self._grafo[parziale[-1]][v]["weight"]
    #             if pesoEdge>self._pesoArco:
    #                 parziale.append(v)
    #                 self._pesoArco = pesoEdge
    #                 self._ricorsione(parziale)
    #                 parziale.pop()

    def searchPath(self, product_number):
        nodoSource = self._idProducts_Map[product_number]

        parziale = []

        self.ricorsione(parziale, nodoSource, 0)

        print("final", len(self._solBest), [i[2]["weight"] for i in self._solBest])

    def ricorsione(self, parziale, nodoLast, livello):
        archiViciniAmmissibili = self.getArchiViciniAmm(nodoLast, parziale)

        if len(archiViciniAmmissibili) == 0: #COND. FINALE E' CHE NON HO PIù ARCHI DA AGGIUNGERE
            if len(parziale) > len(self._solBest):
                self._solBest = copy.deepcopy(parziale)
                print(len(self._solBest), [ii[2]["weight"] for ii in self._solBest])

        for a in archiViciniAmmissibili:
            parziale.append(a)
            self.ricorsione(parziale, a[1], livello + 1)
            parziale.pop()

    #qui è parte principale della ricorsione:
    def getArchiViciniAmm(self, nodoLast, parziale):

        archiVicini = self._grafo.edges(nodoLast, data=True) #EDGES E CI METTO IL NODO E DATA = TRUE MI DA GLI ARCHI CHE COMPRENDONO QUEL NODO
        result = []
        for a1 in archiVicini:
            if self.isAscendent(a1, parziale) and self.isNovel(a1, parziale):
                result.append(a1)
        return result

    def isAscendent(self, e, parziale):#VERIFICA CHE IL PESO DEL NODO D'AGGIUNGERE SIA MAGGIORE DI QUELLO CHE HO GIA
        if len(parziale) == 0:
            print("parziale is empty in isAscendent")
            return True
        return e[2]["weight"] >= parziale[-1][2]["weight"]#CONDIZIONE DA RISPETTARE E' CHE ARCO VICINO(2 INDICA 3 ELEMENTO LISTA E WEIGHT CHIAVE DEL DIZIONARIO),
    #SIA MAGGIORE DEL'ULTIMO ARCO IN PARZIALE E POI DI NUOVO PRENDO (2 CHE INDICA IL DIZIONARIO E WEIGHT LA CHIAVE)

    def isNovel(self, e, parziale):
        if len(parziale) == 0:
            print("parziale is empty in isnovel")
            return True
        e_inv = (e[1], e[0], e[2])
        return (e_inv not in parziale) and (e not in parziale)#Il metodo verifica se né e né e_inv sono presenti in parziale.
        # Se entrambi non sono presenti, il metodo restituisce True, indicando che l'arco e è nuovo. Altrimenti, restituisce False

    def crea_grafo(self,colore,anno):
        self._prodotti = DAO.get_all_products_color(colore)
        self._grafo.clear()
        self._grafo.add_nodes_from(self._prodotti)
        for prod in self._prodotti:
            self._idProducts_Map[prod.Product_number] = prod

        self.crea_archi(anno)
        #archi_ordinati = sorted(self._grafo.edges,)//////////////////////////////////////////////////ORDINARE GRAFO E PRENDERE I PRIMI TRE E STAMPARLI
        #FALLO IN METODO A PARTE CHE POI RICHIAMI

    def crea_archi(self,anno):
        #vendite = DAO.get_all_sales_peso(anno,u,v,_idProducts_Map)
        self._grafo.clear_edges()
        for u in self._prodotti:
            for v in self._prodotti:
                if u!= v:
                    lista_peso = DAO.get_all_sales_peso(anno,u.Product_number,v.Product_number)
                    if len(lista_peso)>=1:
                        peso = lista_peso[0]
                        if peso > 0:
                            self._grafo.add_edge(u, v, weight=peso)



    def getBest3(self):
        self._listaBest= []
        lista_prodotti = []
        sorted_edges = sorted(self._grafo.edges(data=True), key=lambda x: x[2]['weight'],reverse=True)

        for i in sorted_edges:
            self._listaBest.append((i[0].Product_number,i[1].Product_number,i[2]))

        conteggio_numeri = {}
        # Conta le occorrenze di ogni numero
        if len(self._listaBest) >= 3:
            self._listaBest = self._listaBest[:3]

        for tupla in self._listaBest:
            valori = tupla[:-1]  # Ignora il dizionario
            for numero in valori:
                if numero in conteggio_numeri:
                    conteggio_numeri[numero] += 1

                else:
                    conteggio_numeri[numero] = 1


        #lista_prodotti = [numero for numero, conteggio in conteggio_numeri.items() if conteggio > 1]
        for numero,valore in conteggio_numeri.items():
            if valore>1:
                lista_prodotti.append(numero)

        return self._listaBest, lista_prodotti


    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)






