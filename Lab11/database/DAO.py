from database.DB_connect import DBConnect
from model.go_daily_sales import GoDailySales
from model.go_products import Go_Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_colors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT (Product_color) 
                FROM go_products gp"""

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["Product_color"])


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_products_color(colore):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT  DISTINCT * 
                FROM go_products gp
                WHERE gp.Product_color = %s"""

        cursor.execute(query, (colore,))

        for row in cursor:
            result.append(Go_Product(**row))


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_sales_peso(anno,u,v):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count( distinct gds1.`Date`) as peso
                from go_daily_sales gds1, go_daily_sales gds2
                where gds1.Retailer_code = gds2.Retailer_code and year (gds1.Date)=%s
                and gds1.`Date` = gds2.`Date` and gds1.Product_number = %s and gds2.Product_number = %s
                group by gds1.Product_number,gds2.Product_number
"""

        cursor.execute(query, (anno,u,v,))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()
        return result

