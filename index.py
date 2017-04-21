# coding: utf8
from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask import session
from flask import Response
from db import Database
import hashlib
import uuid
from functools import wraps
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from itsdangerous import URLSafeTimedSerializer


app = Flask(__name__)
courriel = None

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

app.secret_key = "(*&*&322387heqe738220)(*(*22347657" 
@app.route('/administration')
def start_page():
    articles = get_db().get_articles()
    username = None
    if "id" in session:
        username = get_db().get_session(session["id"])
    return render_template('admin.html', username=username, articles = articles)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['utilisateur']
    password = request.form['password']
    if username == "" or password == "":
        return render_template('authentifier.html', resultat = "tous les champs sont obligatoires")
    reponse = get_db().verifier(username, password)

    if reponse.reponse == "autorise" :
        id_session = uuid.uuid4().hex
        
        get_db().save_session(id_session, username)
        session["id"] = id_session
        
        return redirect('/administration')
    elif reponse.reponse == "mpincorrect":
        return render_template('authentifier.html', resultat = "mpincorrect")
    else :
        return render_template('authentifier.html', resultat = "introuvable")
@app.route('/confirmation')

def confirmation_page():
    return render_template('confirmer.html')


@app.route('/formulaire', methods=["GET", "POST"])
def formulaire_creation():
    if request.method == "GET":
        return render_template("formulaire.html")
    else:
        email = request.form["email"]

        if email == "":
            return render_template("formulaire.html",
                                   error="Tous les champs sont obligatoires.")
        else:
            token = uuid.uuid4().hex      
            get_db().create_token(token, email)
            url = ("http://localhost:5000/confirm/%s"%token)
            source_address = "omar.djani@gmail.com"
            destination_address = email
            body = (" veuillez cliquer sur le lien pour confirmer votre compte %s " %url)
            subject = "création du compte"
            
 
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = source_address
            msg['To'] = destination_address
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(source_address, "consultation88")
            text = msg.as_string()
            server.sendmail(source_address, destination_address, text)
            server.quit()
            return redirect("/confirmation")

def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return send_unauthorized()
        return f(*args, **kwargs)
    return decorated 

@app.route('/logout')
@authentication_required
def logout():
    if "id" in session:
        id_session = session["id"]
        session.pop('id', None)
        get_db().delete_session(id_session)
    return redirect("/")

def is_authenticated(session):
    return "id" in session


def send_unauthorized():
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

@authentication_required       
@app.route('/admin-nouveau')
def newPost():
    if "id" in session:
        return render_template('nouveau-article.html')
    else: 
        return render_template('authentifier.html'),401
      

@authentication_required    
@app.route('/admin')
def loginAdmin():
    if "id" in session:
        return redirect ('/administration')
    else:
        return render_template('authentifier.html')
        
        
@app.route('/error')
def erreur():
    return render_template('erreur.html')


@app.route('/modifier/<identifiant>')
def modifier(identifiant):
    if "id" in session:
        article = get_db().get_article(identifiant)
        if article is None:
            return render_template('erreur.html'), 404
        else:
            return render_template('modifier.html', article=article)
    else:
        return "",401

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

@app.route('/confirm/<token>')
def confirm_email(token):
    check_token = get_db().check_token(token)
    
    if check_token == False:
        return redirect ('/erreur'),401
    else:
        get_db().delete_token(token)
        return render_template('registration.html')

@app.route('/login_email', methods=['POST'])
def registr():
    username = request.form['utilisateur']
    password = request.form['password']
    email = request.form['email']
    if username == "" or password == "" or email == "":
        return render_template('registration.html', resultat = "tous les champs sont obligatoires"),403
    reponse = get_db().get_user_login_info(username) 
    if reponse is None:
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(password + salt).hexdigest()
        get_db().create_user(username, email, salt, hashed_password)
        return render_template('confirmer.html')
    else:
        return render_template('registration.html', resultat = "utilisateur existe deja ! "),403   
        
@app.route('/mot_passe_oublie')    
def password():
    return render_template('mot_passe.html')

@app.route('/email_forgotten', methods=['POST'])
def forget_email():
    email = request.form['email']
    reponse = get_db().get_user_login_email(email) 
    if reponse is True:
        token = uuid.uuid4().hex      
        get_db().create_token(token, email)
        url = ("http://localhost:5000/initialisation/%s"%token)
        source_address = "omar.djani@gmail.com"
        destination_address = email
        body = (" veuillez cliquer sur le lien pour confirmer votre compte %s " %url)
        subject = "récupération de mot de passe"
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = source_address
        msg['To'] = destination_address
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(source_address, "consultation88")
        text = msg.as_string()
        server.sendmail(source_address, destination_address, text)
        server.quit()
        return redirect("/confirmation")
    else:
        resultat='email inexistant !'
        return render_template('mot_passe.html', resultat = resultat),401    
    
@app.route('/initialisation/<token>')
def confirm_mp(token):
    check_token = get_db().check_token(token)
    
    if check_token == False:
        return redirect ('/erreur')
    else:
        email = get_db().get_email(token)
        get_db().delete_token(token)
        return render_template('initialisation.html', email = email) 
        
    
     
@app.route('/set_password/<email>', methods=['POST'])
def set_password(email): 
        email= email[3:]
        email=email[:-3]
        print email
        passw = request.form['password']
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(passw + salt).hexdigest()   
        get_db().set_passw(salt, hashed_password, email)
        return render_template('confirmer.html')
        
@app.route('/<other>')
def page_404(other):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
  
