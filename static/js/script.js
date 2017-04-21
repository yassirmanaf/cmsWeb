/**
 * Created by Yassir on 2017-04-15.
 */



function onTitreChange() {
    var titre = document.getElementById("titre");
    var identifiant = document.getElementById("idArticle");
    var erreur = document.getElementById("p_error");

    var id2 = titre.value.replace(/\s/g, '-');
    var id_correcte = id2.replace(/[^a-z0-9--]/gmi, "").toLowerCase();


    var xhr = new XMLHttpRequest();

    xhr.open("POST", "/identifiant/" + id_correcte, true);
    xhr.send();

    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.status == 200) {


                if (xhr.responseText == id_correcte) {

                    identifiant.value = id_correcte;
                    erreur.hidden = true;
                } else {

                    identifiant.value = id_correcte + "1";
                    erreur.hidden = true;
                }

            } else {
                console.log('erreur avec server');
            }
        }
        ;
    }
}


function onIdChange() {
    var identifiant = document.getElementById("idArticle");
    var erreur = document.getElementById("p_error");
    var id_correcte = identifiant.value.toLowerCase().replace(/[?]/g, "");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/identifiant/" + id_correcte, true);
    xhr.send();

    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.status == 200) {
                //onIdChange()
                if (!(xhr.responseText == id_correcte )) {
                    erreur.hidden = false;
                    erreur.innerHTML = xhr.responseText;
                } else {
                    console.log('dekht');
                    erreur.hidden = true;
                    identifiant.value = id_correcte;
                }

            } else {
                console.log('erreur avec server');

            }
        }
        ;
    }
}