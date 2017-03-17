import sqlite3
import re
from ObjetArticle import Article


def build_artist_dictionary(row):
    return {"titre": row[0], "identifiant": row[1], "auteur": row[2],
            "date_publication": row[3], "paragraphe": row[4]}


class Database:

    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('DB/cms.bd')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def insert_article(self, title, identifiant, author, publish_date, parag):

        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into article(titre, identifiant, "
                        "auteur, date_publication, paragraphe)"
                        "values(?,?,?,?,?)"), (title, identifiant, author,
                                               publish_date, parag))
        connection.commit()

    def update(self, identifier, title, parag):

        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(" update article set titre = ? , "
                       "paragraphe = ? where identifiant = ? ",
                       (title, parag, identifier,))
        connection.commit()

    def is_unique_id(self, identifier):

        connection = self.get_connection()
        cursor = connection.cursor()
        identifiant = cursor.execute(" select identifiant from article "
                                     "where identifiant = ?",
                                     (identifier,)).fetchall()
        if len(identifiant) == 0:
            return True
        else:
            return False

    def get_article_accueil(self, cherche):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article "
                       "WHERE titre LIKE ? OR paragraphe LIKE ?",
                       ('%'+cherche+'%', '%'+cherche+'%',))
        articles = cursor.fetchall()
        liste = []

        for titre in articles:
            titres = Article(titre[1], titre[2], titre[3], titre[4], titre[5])
            liste.append(titres)

        return liste

    def get_fiveArticle(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article "
                       "WHERE date_publication <= date() ")
        articles = cursor.fetchall()
        liste = []
        list = []
        i = 0
        for titre in articles:
            titres = Article(titre[1], titre[2], titre[3], titre[4], titre[5])
            liste.append(titres)
        liste.sort(key=lambda r: r.date_publication, reverse=True)
        for object in liste:
            if i < 5:
                list.append(object)
                i = i + 1
        return list

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
            "select titre, identifiant, auteur, date_publication, "
            "paragraphe "
            "from article where identifiant = ?",
            (identifier,)).fetchone()
        if article is None:
            return None
        else:
            return build_artist_dictionary(article)

    def get_articles(self):
        cursor = self.get_connection().cursor()
        articles = cursor.execute(
            "select titre, identifiant, auteur, date_publication, "
            "paragraphe from article").fetchall()
        return [build_artist_dictionary(each) for each in articles]
