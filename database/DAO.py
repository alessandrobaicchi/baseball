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
