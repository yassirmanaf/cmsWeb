import sqlite3
import re

def build_artist_dictionary(row):
    return {"titre":row[0], "identifiant":row[1], "auteur":row[2], "date_publication":row[3], "paragraphe":row[4]}




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

    def update(self, identifier, title, parag):

        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(" update article set titre = ? , paragraphe = ? where identifiant = ? ",
                       (title, parag, identifier,))
        connection.commit()

    def is_unique_id(self, identifier):

        connection = self.get_connection()
        cursor = connection.cursor()
        identifiant = cursor.execute(" select identifiant from article where identifiant = ?", (identifier,)).fetchall()
        if len(identifiant) == 0:
            return True
        else:
            return False

    def valid_date(self, datestring):
        try:
            mat = re.match('(\d{4})[-](\d{2})[-](\d{2})$', datestring)
            if mat is not None:
                return True
        except ValueError:
            pass
        return False

    def valid_id(self, identifier):
        try:
            mat = re.match('^[a-zA-Z0-9][ A-Za-z0-9._-]*$', identifier)
            if mat is not None:
                return True
        except ValueError:
            pass
        return False

    def get_article(self, identifier):
        cursor = self.get_connection().cursor()
        article = cursor.execute(
            "select titre, identifiant, auteur, date_publication, paragraphe from article where identifiant = ?",
            (identifier,)).fetchone()
        if article is None:
            return None
        else:
            return build_artist_dictionary(article)

    def get_articles(self):
        cursor = self.get_connection().cursor()
        articles = cursor.execute(
            "select titre, identifiant, auteur, date_publication, paragraphe from article").fetchall()
        return [build_artist_dictionary(each) for each in articles]


    