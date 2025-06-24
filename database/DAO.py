from database.DB_connect import DBConnect
from model.arco import Arco
from model.artObject import ArtObject


class DAO():

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """select * from objects o"""

        cursor.execute(query)

        for row in cursor:
            result.append(ArtObject(**row))
            # **row per fare unpack dei parametri di row (se i nomi sono uguali)
            # si potrebbe scrivere anche in forma estesa

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getPeso(v1, v2):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """select eo.object_id, eo2.object_id, count(*) as peso
                    from exhibition_object eo, exhibition_objet eo2
                    where eo.exhibition_id = eo2.exhibition_id and eo.object_id < eo2.object_id and eo.object_id = %s and eo2.object_id = %s
                    group by eo.object_id, eo2.object_id"""
        # < per avere le coppie che voglio (una sola volta)

        cursor.execute(query, (v1.object_id, v2.object_id))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()

        if len(result) == 0:
            return None

        return result

    @staticmethod
    def getAllArchi(idMap): # per recuperare gli oggetti dagli id
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """select eo.object_id as o1, eo2.object_id as o2, count(*) as peso
                    from exhibition_objects eo, exhibition_objects eo2
                    where eo.exhibition_id = eo2.exhibition_id and eo.object_id < eo2.object_id
                    group by eo.object_id, eo2.object_id
                    order by peso desc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Arco(idMap[row["o1"]], idMap[row["o2"]], row["peso"]))

        cursor.close()
        conn.close()

        if len(result) == 0:
            return None

        return result