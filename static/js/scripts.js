jQuery('[data-toggle="popover"]').popover();
function hideItemAdded(){
    jQuery(".item_added").trigger("click");
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
// popup notifitaction when we add a new item into the cart.

/*
$(".login_element").click(function(e){
    e.preventDefault();
    $('#login form').slideToggle(300);
    $(this).toggleClass('close');
});
*/