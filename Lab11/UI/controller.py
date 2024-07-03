import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        #riempo dropdown degli anni
        self._listYear= [2015,2016,2017,2018]
        for anno in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(anno))

        #riempio dropdown dei colori
        self._listColor = self._model._colori
        for colore in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(colore))

        self._view.update_page()
    def controllo(self,contr):
        if contr == None or contr == 0 or contr =="":
            raise ValueError("Elemento vuoto")

    def handle_graph(self, e):
        try:
            colore = self._view._ddcolor.value
            year = self._view._ddyear.value
            self.controllo(year)
            self.controllo(colore)
        except ValueError:
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text("Inserisci i dati correttamente"))
            self._view.update_page()
            return


        self._model.crea_grafo(colore,year)
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text(f"Per l'anno {year} e il colore {colore} creato il grafo:"))
        self._view.txtOut.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodes()}"))
        self._view.txtOut.controls.append(ft.Text(f"Numero di archi: {self._model.getNumEdges()}"))
        migliori, lista_prod = self._model.getBest3()
        for i in migliori:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {i[0]} a {i[1]} con peso {i[2]["weight"]}"))
        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono {lista_prod}"))

        self._view._ddnode.disabled = False
        self._view.btn_search.disabled = False
        self.fillDDProduct()

        self._view.update_page()





    def fillDDProduct(self):
        nodi = self._model._grafo.nodes
        for n in nodi:
            self._view._ddnode.options.append(ft.dropdown.Option(n.Product_number))

        self._view.update_page()

    def handle_search(self, e):
        nodo = self._view._ddnode.value
        if nodo == None or nodo == "":
            self._view.txtOut2.controls.clear()
            self._view.txtOut2.controls.append(ft.Text(f"Seleziona un nodo"))
            self._view.update_page()
            return
        else:
            self._model.searchPath(int(nodo))
            self._view.txtOut2.controls.append(ft.Text(f"lunghezza percorso {len(self._model._solBest)}"))

        self._view.update_page()
