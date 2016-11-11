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
    if(username != "" && password !=""){
      alert("entree correcte");
    }
    else{
      alert("Veuillez saisir le nom d'utilsateur et le mot de passe.");
      return false;
    }
  });
}
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
