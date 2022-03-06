/*
23/01/2022
@author: Tony Quedeville
Studi.com
Bachelor développeur d'application Python.
Evaluation: BDACSDEXA21A (Gestion de liste)
*/


let pseudo = ''
let motpass = ''

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


