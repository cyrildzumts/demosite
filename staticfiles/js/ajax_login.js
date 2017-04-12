$("#login_form").submit(function(){
    $.ajax({
        type: $(this).attr('method'),
        url : '/api/ajax/ajax_login/',
        data: $('#login_form').serialize(),
        dataType: 'json',
        // success Function called in case of an http 200 response
        success: function(data){
            if(data.status == 200){
                text = "Connexion reussie ";
            }
            else {
                text = "erreur de connexion - veuillez ressayer";
            }
            document.getElementById("server_response").innerHTML = text;
            //alert(text);
        }

    });
});
