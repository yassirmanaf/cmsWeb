from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from db import Database
from flask import g

app = Flask(__name__)


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
<<<<<<< HEAD
@app.route('/')
def Accueil():
    return render_template('Accueil.html')

=======


@app.route('/')
def index():
    articles = get_db().get_articles()
    return render_template('Acceuil.html', articles=articles)


>>>>>>> e83835279fa9194d91b78c991991b6507159cbea
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


<<<<<<< HEAD
=======
@app.route('/send', methods=['POST'])
def donnees_recherchees():
    x = request.form['name']
    articles = get_db().get_article(x)
    print articles
    return render_template('articles.html', article=articles)

>>>>>>> e83835279fa9194d91b78c991991b6507159cbea

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


@app.route('/<other>')
def page_404(other):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
