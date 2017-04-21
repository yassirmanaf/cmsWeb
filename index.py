from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from db import Database
from flask import g
from flask import jsonify


app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/')
def index():
    articles = get_db().get_fiveArticle()
    return render_template('Accueil.html', articles=articles)


@app.route('/admin')
def admin():
    articles = get_db().get_articles()
    return render_template('admin.html', articles=articles)


@app.route('/admin-nouveau')
def newPost():
    return render_template('nouveau-article.html')


@app.route('/error')
def erreur():
    return render_template('erreur.html')


@app.route('/modifier/<identifiant>')
def modifier(identifiant):
    article = get_db().get_article(identifiant)
    if article is None:
        return render_template('erreur.html'), 404
    else:
        return render_template('modifier.html', article=article)


@app.route('/update/<identifier>', methods=['POST'])
def change(identifier):
    article = get_db().get_article(identifier)
    new_titre = request.form['titre']
    new_paragraphe = request.form['paragraphe']
    if '' in (new_titre, new_paragraphe):
        return render_template('modifier.html', article=article,
                               erreur='Tout les champs sont obligatoires')
    else:
        get_db().update(identifier, new_titre, new_paragraphe)
        return redirect('/admin')


@app.route('/send', methods=['POST'])
def donnees_recherchees():
    mot_recherche = request.form['name']
    articles = get_db().get_article_accueil(mot_recherche)
    return render_template('articles.html',
                           articles=articles, mot=mot_recherche)


@app.route('/article/<identifiant>')
def article_page(identifiant):
    article = get_db().get_article(identifiant)
    if article is None:
        return render_template('erreur.html',
                               erreur='Article Introuvable'), 404
    else:
        return render_template('article.html', article=article)


@app.route('/envoyer', methods=['POST'])
def formulaire():
    titre = request.form['titre']
    identifiant = request.form['idArticle']
    auteur = request.form['auteur']
    date = request.form['date']
    paragraphe = request.form['paragraphe']
    if '' in (titre, identifiant, auteur, date, paragraphe):
        return render_template('nouveau-article.html',
                               erreur='Tout les champs sont obligatoires')

    if not get_db().is_unique_id(identifiant):
        return render_template('nouveau-article.html',
                               id_erreur='ID existe deja')

    if not get_db().valid_date(date):
        return render_template('nouveau-article.html',
                               date_erreur='FORMAT DATE INVALIDE')

    if not get_db().valid_id(identifiant):
        return render_template('nouveau-article.html',
                               id2_erreur='ID Non Valide')

    else:
        get_db().insert_article(titre, identifiant, auteur, date, paragraphe)
        return redirect('/admin')


@app.route('/identifiant/<iden>', methods=['POST'])
def identifiant(iden):

    if not get_db().valid_id(iden):
        return render_template('identifiant.html',
                               id2_erreur='ID Non Valide')

    if not get_db().is_unique_id(iden):
        return render_template('identifiant.html',
                               id_erreur='ID existe deja')

    else:
        return iden


@app.route('/identifiant/', methods=['POST'])
def erreur_id():

    return render_template('identifiant.html', id2_erreur='ID Non Valide')


@app.route('/api/articles/', methods=["GET", "POST"])
def liste_article():
    if request.method == "GET":
        articles = get_db().get_articles_json()
        data = [{"titre": each[0], "auteur": each[2],
                 "url":  "/article/" + each[1]} for each in articles]
        return jsonify(data)
    else:
        data = request.get_json()
        if get_db().is_unique_id(data["identifiant"]) \
                and get_db().valid_id(data["identifiant"]):
            get_db().insert_article(data["titre"], data["identifiant"],
                                    data["auteur"],
                                    data["date de publication"],
                                    data["paragraphe"])
            return "", 201
        else:
            return"", 400


@app.route('/api/articles/<identifier>')
def article(identifier):
    article = get_db().get_article_id_json(identifier)
    if article is None:
        return render_template('erreur.html',
                               erreur='Article Introuvable'), 404
    else:
        data = {"titre": article[0], "identifiant": article[1],
                "auteur": article[2], "date de publication": article[3],
                "paragraphe": article[4]}
        return jsonify(data)


@app.route('/<other>')
def page_404(other):
    return render_template('404.html'), 404


@app.route('/api/<other>')
def page_404_api(other):
    return render_template('404.html'), 404


@app.route('/api/doc')
def doc():
    return render_template('doc.html')


if __name__ == "__main__":
    app.run(debug=True)
