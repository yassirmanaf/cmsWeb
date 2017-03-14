import sqlite3

class Database:


    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection= sqlite3.connect('cms.bd')
        return self.connection

    def get_titres(self):
        cursor= self.get_connection().cursor()
        titres= cursor.execute("select titre from article").fetchall()
        identifiant = cursor.execute("select identifiant from article").fetchall()
        auteur = cursor.execute("select auteur from article").fetchall()
        date=cursor.execute("select date_publication from article").fetchall()
        parag=cursor.execute("select paragraphe from article").fetchall()
        return [titre[0] for titre in titres]



    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def insert_article(self,title, identifiant, author, publish_date, parag ):

        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into article(titre, identifiant, auteur, date_publication, paragraphe)"
                        "values(?,?,?,?,?)"),(title, identifiant, author, publish_date, parag))
        connection.commit()
    
    def get_article(self,cherche):
        
        cursor = self.get_connection().cursor()
        cursor.execute("select titre,date_publication from article WHERE titre LIKE ? OR paragraphe LIKE ?", ('%'+cherche+'%', '%'+cherche+'%',))
        articles = cursor.fetchall()
        return [titre[0] + ' - Article publie le: ' + titre[1] for titre in articles]

    