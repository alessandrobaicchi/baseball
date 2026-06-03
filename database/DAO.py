from database.DB_connect import DBConnect
from model.team import Team


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    select distinct (t.`year`) 
                    from teams t 
                    where t.`year` >= 1980
                """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])
            # I risultati della query li leggo direttamente come interi,
            # perché in questo caso non mi serve un oggetto apposta.

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def getTeamsOfYear(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    select *
                    from teams t 
                    where t.year  = %s
                """

        cursor.execute(query, (year,))
        # Il %s viene sostituito da year


        for row in cursor:
            result.append(Team(**row))
            # I risultati della query li metto in un DTO ad hoc.
            # Posso fare l'unpacking (**row) perché i parametri del DTO team hanno lo STESSO NOME
            # delle colonne della tabella teams del DB. Altrimenti avrei dovuto creare l'oggetto Team
            # usando il costruttore per esteso.

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def getSalariesTeam(year, idMapTeams):
        conn = DBConnect.get_connection()

        # result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    select t.ID , t.teamCode , sum(s.salary) as totSalary
                    from salaries s, teams t, appearances a 
                    where s.`year` = t.`year` and t.`year` = a.`year` and a.`year` = %s
                    and t.ID = a.teamID and a.playerID = s.playerID 
                    group by t.ID, t.teamCode
                """

        cursor.execute(query, (year,))
        # Il %s viene sostituito da year

        mapSalary = {}  # E' un dizionario vuoto
        for row in cursor:
            mapSalary[idMapTeams[row["ID"]]] = row["totSalary"]
            # Creo una mapSalary che avrà come chiave il team e come valore la somma dei salari.
            # Il team lo recupero da un idMapTeams (che viene passata al metodo)
            # che mappa la chiave primaria del team con il team stesso.
            # In questo modo l'output di questo metodo è un dizionario che ha come chiavi gli oggetti
            # di tipo team e come valori la somma dei salari ottenuti dalla query.

        cursor.close()
        conn.close()
        return mapSalary
