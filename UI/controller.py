import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceTeam = None

    def handleCreaGrafo(self, e):
        pass

    def handleDettagli(self, e):
        pass

    def handlePercorso(self, e):
        pass


    # Metodo che aggiunge i campi del DD _view._ddAnno
    # Questo metodo lo chiamo nel View subito dopo aver creato _view._ddAnno
    def _fillDDYears(self):
        years = self._model.getAllYears()

        # years contiene interi, ma servono degli oggetti tipo dropdown.Option

        # Metodo 1, il più semplice
        # yearsDD = []
        # for y in years:
        #     yearsDD.append(ft.dropdown.Option(y))

        # Metodo 2, il più elegante
        yearsDD = list(map(lambda x: ft.dropdown.Option(x), years))
        # Map ha due argomenti: una funzione e iterable.
        # Map non fa altro che applicare la funzione all'iterable (qui una lista).
        # Quindi col metodo Map applico la Lambda function agli elementi della lista years:
        # a ogni elemento della lista years applica la funzione ft.dropdown.Option(x).
        # Il risultato è un iterable che metto in una lista che ora posso assegnare alle opzioni del Dropdown.
        self._view._ddAnno.options = yearsDD
        self._view.update_page()


    # Questo metodo viene chiamato quando l'utente ha selezionato un anno.
    # Poi, va a recuperare tutti i team che hanno giocato quell'anno,
    # li stampa nel textfield (_view._txtOutSquadre)
    # e li usa per riempiere il dropdown (self._view._ddSquadra).
    def handleYearSelection(self, e):
        # Uso la scelta fatta dall'utente
        if self._view._ddAnno.value is None:
            self._view._txtOutSquadre.controls.clear()
            self._view._txtOutSquadre.controls.append(ft.Text("Selezionare un anno dal menù",color="red"))

        # Arriva una lista di team
        teams = self._model.getTeamsOfYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Per l'anno {self._view._ddAnno.value} "
                                                          f"sono iscritte al campionato {len(teams)} squadre."))
        for t in teams:
            # Stampa nel _view._txtOutSquadre
            # Sto usando la rappresentazione a stringa (__str__()) della classe Team.
            self._view._txtOutSquadre.controls.append(ft.Text(t))

            # Popolo il DD self._view._ddSquadra
            # self.readDDTeams è "il solito metodo" che usiamo per leggere la scelta dell'utente
            self._view._ddSquadra.options.append(
                ft.dropdown.Option(data = t,
                                   text = t.name,
                                   on_click = self.readDDTeams))

        self._view.update_page()


    def readDDTeams(self, e):
        if e.control.data is None:
            self._choiceTeam = None
        else:
            self._choiceTeam = e.control.data
        print(f"Selezionato il team: {self._choiceTeam}")