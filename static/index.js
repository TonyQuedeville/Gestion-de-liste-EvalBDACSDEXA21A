/*
23/01/2022
@author: Tony Quedeville
Studi.com
Bachelor développeur d'application Python.
Evaluation: BDACSDEXA21A (Gestion de liste)
*/

let pseudo = ''
let motpass = ''

// event Pseudo : identification utilisateur
$("#pseudo").change(function (){
    $.ajax({
        url: "/identificationUtilisateurJson?pseudo=" + $("#pseudo").val(),
        success: identificationUtilisateur,
        error: function (xhr, ajaxOptions, thrownError) {
            console.log("Erreur ajax: readTache()")
            //console.log(thrownError)
          }
    });
})

function identificationUtilisateur(result){console.log(result)
    if( result == 0){
        $("#visiteur").text(texte)
        pseudo = $("#pseudo").val()
    }
    else{
        texte = 'Bonjour '
        if (result[0][4] == 1){texte = texte + "Mme. "}
        else{texte = texte + "Mr. "}
        texte = texte + result[0][2] + ' ' + result[0][1]
        $("#visiteur").text(texte)
        pseudo = $("#pseudo").val()
    }
}


// event "Se connecter"
$("#seConnecter").click(function (){
    pseudo = $("#pseudo").val()
    motpass = $("#motpass").val()

    if (pseudo != '' && motpass != ''){
        $.ajax({
            url: "/connexion?pseudo=" + pseudo + "&motpass=" + motpass,
            success: function (response){
                console.log(response)
                    if (response == 0){alert("Mot de passe incorrecte !")}
                    else{window.location.href="/taches"}
                },
            error: function (xhr, ajaxOptions, thrownError) {
              console.log(thrownError)
              }
        });
    }else{
        alert("Veuillez entrer un pseudonyme et le mot de passe svp !")
    }
});
/*-*/



