from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from db import Database
from flask import g


app = Flask (__name__)

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
        
@app.route('/accueil')
def Accueil():
    return render_template('Accueil.html')


@app.route('/')
def index():
    titres = get_db().get_titres()

    return render_template('index.html', titres=titres )

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin-nouveau')
def newPost():
    return render_template('nouveau-article.html')

@app.route('/error')
def erreur():
    return render_template('erreur.html')

@app.route('/envoyer' , methods=['POST'])
def formulaire():
    titre= request.form['titre']
    identifiant= request.form['idArticle']
    auteur = request.form['auteur']
    date = request.form['date']
    paragraphe = request.form['paragraphe']

    if '' in (titre , identifiant, auteur , date , paragraphe):
        return render_template('nouveau-article.html',erreur='Tout les champs sont obligatoires', value=titre)



    else:
        get_db().insert_article(titre, identifiant, auteur, date, paragraphe)
        return redirect('/thanks')

@app.route('/send', methods=['POST'])
def donnees_recherchees():
    x = request.form['name']
    
    articles = get_db().get_article(x)
    print articles
    return render_template('articles.html', articles=articles)







if __name__ == "__main__":
    app.run(debug=True)
