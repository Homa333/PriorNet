import mysql.connector

class DbmsConnect:
    def __init__(self, database_name):
        self.mydb = mysql.connector.connect(host="localhost", user="root", password="root123", database=f"{database_name}")
        self.data = {}
        self.mycursor = self.mydb.cursor()

    def insert_into_database(self, cmd):
            self.mycursor.execute(cmd)
            self.mydb.commit()

    def get_data_from_database(self, cmd):
            self.mycursor.execute(cmd)
            self.data = self.mycursor.fetchall()



