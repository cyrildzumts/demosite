function addToCart2(id){
    $.ajax({
        type: 'POST',
        url : '/cart/add_to_cart/',
        data: {product_id: id},
        dataType: 'json',
        // success Function called in case of an http 200 response
        success: item_add_confirm,
        error: function (){
            alert("Il y a une erreur, Veuillez reessayer.");
        }
    });

}
function item_add_confirm(response){
    data = JSON.parse(response);
    alert("Item ajouter dans le Panier . " + data );
    //update the cart icon counter
    update_cart_icon(data);
}

function update_cart_icon(count){
jQuery(".cart_badge").html(count);
}

function addToCart(){
  // code add an item into the Cart
  jQuery("form.addToCart").submit(function(){
    quantity = jQuery("#quantity").val();
    if (!((quantity != "") && (parseInt(quantity) > 0))){
      // invalide data , pop up alert
      // stop submission of form
      alert("Valeur incorrecte: " + quantity);
      return false;
    }
    else {
      alert("Quantité correcte: " + quantity);
    }
  });
}

// display an error message when the
function displayLoginError(){
  jQuery("form.login").submit(function(){
    username = jQuery("#username").val();
    password = jQuery("#password").val();
    if(!(username != "" && password !="")){
        alert("Veuillez saisir le nom d'utilsateur et le mot de passe.");
        return false;
    }
  });
}

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});

$(".dropdown").mouseenter(function(){
    //alert("You entered this cat!");
    $(this).find("ul").fadeIn();
    //$(".dropdown-menu").fadeIn("slow");
});
$(".dropdown").mouseleave(function(){
    //alert("You entered this cat!");
    $(this).find("ul").fadeOut();
    //$(".dropdown-menu").fadeIn("slow");
});
//jQuery(document).ready(addToCart);
jQuery(document).ready(displayLoginError);

// popup notifitaction when we add a new item into the cart.
