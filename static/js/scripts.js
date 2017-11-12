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



function Cart (){
    this.username = "";
    this.cartID = 0;
    this.count = 0;
    this.total = 0;
    this.items = [];
    this.observers = [];
    this.setUsername = function(username){
        this.username = username;
    }
    this.setCartID = function(id){
        this.cartID = id;
    }
    this.setCount = function(count){
        this.count = count;
    }
    this.getTotal = function(){
        return this.total;
    }
    this.notify = function(){
        for(observer in this.observers){
            observer.update();
        }
    }
    this.attach = function(observer){
        this.observers.add(observer);
    }
    this.addItem = function(item){
        this.count = this.count + item.quantity();
        this.total = this.total + item.total;
        this.items.add(item);
        this.notify();
    }

    this.removeItem = function(id){
        var old_count = this.count;
        this.items = this.items.filter(function(item){
            var flag = false;
            if(item.id === id){
                flag = true;
                this.total = this.total - item.total;
                this.count = this.count - item.quantity();
            }
            return flag;
        });
        if(this.count != count){
            this.notify();
        }
        
    }
    this.removeAll = function(){
        this.total = 0;
        this.count = 0;
        while(this.items.lenght){
            this.items.pop();
        }
    }
};

function  ShoppingApp (){
    // Private attibutes :
    this.username = "";
    this.email = "";
    this.loginstate= false;


    this.getUsername = function(){
        return this.username;
    }
    this.getEmail = function(){
        return this.email;
    }
    this.setUsername = function(username){
        this.username = username;
    }
    this.setEmail = function(email){
        this.email = email;
    }
    this.isLoggedIn = function(){
        return this.loginstate == true;
    }
    

    // Cart 
    //this.Cart 
};