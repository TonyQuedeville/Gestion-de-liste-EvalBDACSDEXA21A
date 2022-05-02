/*
23/01/2022
@author: Tony Quedeville
Studi.com
Bachelor développeur d'application Python.
Evaluation: BDACSDEXA21A (Gestion de liste)
*/
/*------------------------------------------------------------------------------------------*/


/* Date du jour par défaut */
const date = new Date();
// formatage de la date 01-02-2022
let jour = date.getDate();
let mois = date.getMonth()+1;
let annee = date.getFullYear();
if (mois < 10) mois = "0" + mois;
if (jour < 10) jour = "0" + jour;

let aujourdhui = annee + "-" + mois + "-" + jour;
/*-*/
let pseudo = ''
let idUtilisateur = ''
/*-*/

/* Initialisation de la page */
$(document).ready(function(){
    idUtilisateur = $("#idUtilisateur").text()
    pseudo = $("#pseudo").text()

    // Si utilsateur non reconnu : Visiteur
    if(idUtilisateur == ''){
        $("#supprimeTache").hide()
        $("#valideTache").hide()
        $("#nouvelleTache").hide()
        $("#statusTache").attr('disabled', true)
        $("#dateTache").attr('disabled', true)
    }

    // initialisation des filtres
    $("#calendrier").val(aujourdhui)
    tachesDuJour() //Recherche des taches du jours par défaut.
})
/*-*/


/* Evenements */
 $("#nouvelleTache").click(function (){
    // effacement tache
    $("#idTache").text('')
    $("#nomTache").val('')
    $("#descripTache").val('')
    $("#statusTache").val('')
    $("#dateTache").val(aujourdhui)
    $("#nomTache").focus()
})


/* CRUD */
    /* Créer */
    function nouvelleTache(){
        if($("#nomTache").val() && $("#dateTache").val()){
            $.ajax({
                url: "/initTachesJson?nomTache=" + $("#nomTache").val() +
                                    "&descripTache=" + $("#descripTache").val()  +
                                    "&dateTache=" + $("#dateTache").val() +
                                    "&statusTache=" + $("#statusTache").val() +
                                    "&idUtilisateur=" + idUtilisateur,
                success: creerTache,
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log("Erreur ajax: creerTache()")
                    //console.log(thrownError)
                  }
            });
        }
        else{alert("Erreur ! Une nouvelle tâche doit comporter au moins un titre et une date.")}
    }
    /*---*/

    function creerTache(result){
        if(result['idTache'] == 0){alert("Erreur requète ! Nouvelle tâche non prise en compte.")}
        else{$("#idTache").text(result['idTache'])}
    }

    /* Valider */
    $("#valideTache").click(function (){
        // Modifier
        if($("#nomTache").val() && $("#dateTache").val()){
            if($("#idTache").text()){
                $.ajax({
                    url: "/updateTachesJson?idTache=" + $("#idTache").text() +
                                        "&dateTache=" + $("#dateTache").val() +
                                        "&nomTache=" + $("#nomTache").val() +
                                        "&descripTache=" + $("#descripTache").val() +
                                        "&statusTache=" + $("#statusTache").val(),
                    success: updateTaches,
                    error: function (xhr, ajaxOptions, thrownError) {
                        console.log("Erreur ajax: updateTaches()")
                        //console.log(thrownError)
                      }
                });

                function updateTaches(result){
                    if (result == 0){alert("Erreur requète ! Validation non prise en compte.")}
                    else{alert("Tâche validé !")}
                }
            }
            // Créer
            else {
                nouvelleTache()
            }
        }
        else{alert("Erreur ! Une nouvelle tâche doit comporter au moins un titre et une date.")}
    })
    /*---*/


    /* Lire */
      // Selection de date
        $("#calendrier").change(function (){
            tachesDuJour()
        })

        function tachesDuJour(){
            $.ajax({
                url: "/readTachesJson?dateTache=" + $("#calendrier").val(),
                success: readTaches,
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log("Erreur ajax: readTache()")
                    //console.log(thrownError)
                  }
            });
        }

        function readTaches(result){
                $("#filtrePseudo").remove()
                $("#listeTache").remove()
                stat(result['stat'][0])

                if( result['numTache'].length > 0){
                    $("#pseudos").append(`
                        <select name="filtrePseudo" id="filtrePseudo">
                            <option value=""></option>
                        </select>
                    `)
                    $("#taches").append(`
                        <select name="listeTache" id="listeTache">
                            <option value=""></option>
                        </select>
                    `)

                    // Select filtre pseudo
                    for(i=0; i<result['pseudoUnique'].length; i++){
                        $("#filtrePseudo").append(`
                            <option value="${result['pseudoUnique'][i][0]}">${result['pseudoUnique'][i][1]}</option>
                        `)
                    }

                    // Liste de taches
                    for(i=0; i<result['numTache'].length; i++){
                        $("#listeTache").append(`
                            <option value="${result['tache'][i][0]}">${result['tache'][i][1]} : (${result['tache'][i][7]})</option>
                        `)
                    }
                }
                // effacement tache
                $("#idTache").text('')
                $("#nomTache").val('')
                $("#descripTache").val('')
                $("#statusTache").val('')
                $("#dateTache").val(aujourdhui)
            }
      // ---

      // Select filtre Pseudos
        $("#pseudos").on('change','#filtrePseudo', function (){
            $.ajax({
                url: "/readTachesJson?idUtilisateur=" + $("#filtrePseudo").val()  +
                                    "&dateTache=" + $("#calendrier").val(),
                success: filtreTachePseudo,
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log("Erreur ajax: readTache()")
                    //console.log(thrownError)
                  }
            });
        })

        function filtreTachePseudo(result){
            stat(result['stat'][0])
            $("#listeTache").remove()
            if( result['numTache'].length > 0){
                $("#taches").append(`
                    <select name="listeTache" id="listeTache">
                        <option value=""></option>
                    </select>
                `)
                // Liste de taches
                for(i=0; i<result['numTache'].length; i++){
                    $("#listeTache").append(`
                        <option value="${result['tache'][i][0]}">${result['tache'][i][1]} : (${result['tache'][i][7]})</option>
                    `)
                }
            }
            $("#idTache").text('')
            $("#nomTache").val('')
            $("#descripTache").val('')
            $("#statusTache").val('')
            $("#dateTache").val(aujourdhui)
        }


      // Select filtre liste de taches
        $("#taches").on('change','#listeTache', function (){
            $.ajax({
                url: "/readTachesJson?idTache=" + $("#listeTache").val() +
                                    "&idUtilisateur=" + $("#filtrePseudo").val()  +
                                    "&dateTache=" + $("#calendrier").val(),
                success: readTache,
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log("Erreur ajax: readTache()")
                    //console.log(thrownError)
                  }
            });
        })

        function readTache(result){
            console.log(result)
            if( result['numTache'].length > 0){
                $("#idTache").text(result['tache'][0][0])
                $("#nomTache").val(result['tache'][0][1])
                $("#descripTache").val(result['tache'][0][4])
                $("#statusTache").val(result['tache'][0][3])

                const dtTache = new Date(result['tache'][0][2])
                let moisTache = dtTache.getMonth(result['tache'][0][2])+1 //+1: Janvier = 0
                if (moisTache < 10) moisTache = "0" + moisTache;
                let jourTache = dtTache.getDate(result['tache'][0][2])
                if (jourTache < 10) jourTache = "0" + jourTache;
                const dateTache = dtTache.getFullYear(result['tache'][0][2])
                                + "-" + moisTache + "-" + jourTache
                $("#dateTache").val(dateTache)
            }
            else{
                $("#idTache").text('')
                $("#nomTache").val('')
                $("#descripTache").val('')
                $("#statusTache").val('')
                $("#dateTache").val(aujourdhui)
            }
        }
      // ---
    /*---*/


    /* Supprimer */
    $("#supprimeTache").click(function (){
        $.ajax({
            url: "/deleteTachesJson?idTache=" + $("#idTache").text(),
            success: deleteTache,
            error: function (xhr, ajaxOptions, thrownError) {
                console.log("Erreur ajax: deleteTache()")
                //console.log(thrownError)
              }
        });

        function deleteTache(result){
            if (result == 1){alert("Tâche supprimée !")}
                else{alert("Erreur requète ! Suppression non prise en compte.")}
        }
    })
    /*---*/

/*---*/

/* Initialiser les filtres */
$("#sansFiltre").click(function(){
    $("#calendrier").val('')
    $("#filtrePseudo").val('')
    tachesDuJour()
})


/* Mise à jour du Status tache */
$("#statusTache").change(function (){

    if($("#idTache").text()){
        $.ajax({
            url: "/updateTachesJson?idTache=" + $("#idTache").text() +
                                "&statusTache=" + $("#statusTache").val(),
            success: updateTaches,
            error: function (xhr, ajaxOptions, thrownError) {
                console.log("Erreur ajax: updateTaches()")
                //console.log(thrownError)
              }
        });

        function updateTaches(result){
            if (result == 0){alert("Erreur requète ! Validation non prise en compte.")}
        }
    }
})

/* Affichage des statistiques de progression */
function stat(result) {
    $("#afaire").val(result[0])
    $("#encours").val(result[1])
    $("#terminee").val(result[2])
    $("#annulee").val(result[3])
    $("#valafaire").text('à faire: ' + result[0] + '%')
    $("#valencours").text('en cours: ' + result[1] + '%')
    $("#valterminee").text('terminée: ' + result[2] + '%')
    $("#valannulee").text('annulée: ' + result[3] + '%')
}
