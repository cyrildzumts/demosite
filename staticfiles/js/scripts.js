

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
$(".search-form").submit(function(){
    var q = document.forms["search-form"]["q"].value;
    if(q == "")
        return false;
    return true;
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
// popup notifitaction when we add a new item into the cart.

/*
$(".login_element").click(function(e){
    e.preventDefault();
    $('#login form').slideToggle(300);
    $(this).toggleClass('close');
});
*/

/**
 * Open The menu by setting the menu's width.
 */

 /*
function openMenu(){
    document.getElementById("site-menu").style.width = "250px";
}

function closeMenu(){
    document.getElementById("site-menu").style.width = "0";
}

*/
$("#openMenu").click(function(){
    document.getElementById("site-menu").style.width = "250px";
    document.body.style.backgroundColor = "rgba(0,0,0.4,0.4)";
});
$(".close").click(function(){
    document.getElementById("site-menu").style.width = "0";
    document.body.style.backgroundColor = "white";
    
});
$("#loginBtn").click(function(){
    $("#loginModal").modal();
});
$("#loginBtn2").click(function(){
    $("#loginModal").modal();
});




var Cart = (function(){
    function Cart(){
        this.events = [];
        this.items = [];
        this.eventListeners = [];
        this.total = 0;
        this.count = 0;
        this.userID = -1;
        this.observers = [];
        this.serverUrl = "";
    }
    Cart.prototype.initDefault = function(){
        jQuery(".add-to-cart").click(this.onAddButtonClicked.bind(this));
        jQuery(".plusButton").click(this.onPlusButtonClicked.bind(this));
        jQuery(".minusButton").click(this.onMinusButtonClicked.bind(this));
        jQuery(".removeFromCartButton").click(this.onRemoveButtonClicked.bind(this));
        //jQuery(".cart-popover-button").hover(function(){
        //jQuery("#cart-modal").modal({backdrop: false});
       // });
       jQuery(".cart-button").hover(this.onCartButtonHover.bind(this));
    };
    Cart.prototype.init = function(listener){
        this.addEventListener(listener);
    };
    Cart.prototype.onCartButtonHover = function(event){
        console.log("Cart hovered ..");
        $(".cart-button").dropdown();
    };
    Cart.prototype.onAddButtonClicked = function(event){
        var item = {};
        var element = jQuery(".add-to-cart");
        item.id = parseInt(element.attr("data-itemid"));
        item.is_available = element.attr("data-available");
        item.price = 15000;
        item.quantity = 1;
        console.log("Event targert :"+  event.target.nodeName);
        this.addItem(item);
    };
    Cart.prototype.onRemoveButtonClicked = function(event){
        console.log("RemovedButton Clicked ...");
        var $target_parent = $(event.target).parent();
        var itemID = parseInt($target_parent.attr("data-itemid"));
        var that = this;

        $.ajax({
            type: 'POST',
            url: '/cart/cart_update/',
            data: {product_id: itemID, quantity : 0},
            dataType:'json',
            success: function(response){
                that.total = response.total;
                that.count = response.count;
                $target_parent.parent().remove();
                that.notify({});
            },
            error: function(response){
                console.log("Error : couldn't remove the  article");
            }
        });
    };
    Cart.prototype.onPlusButtonClicked = function(event){
        console.log("PlusButton Clicked ...  : ");
        var itemID = parseInt($(event.target).parent().attr("data-itemid"));
        var price = parseFloat($(event.target).parent().attr("data-price"));
        var quantity = parseInt($(event.target).prev().html());
        var total_price_element = $(event.target).parent().siblings(".cart-item-total-price");

        var target = $(event.target).prev();
        var that = this;
        $.ajax({
            type: 'POST',
            url: '/cart/cart_update/',
            data: {product_id: itemID, quantity : quantity + 1},
            dataType:'json',
            success: function(response){
                that.total = response.total;
                that.count = response.count;
                $(target).html(quantity + 1);
                $(total_price_element).html((price * (quantity + 1)) + " FCFA");
                that.notify({});
            },
            error: function(response){
                console.log("Error : couldn't add up article");
            }
        });
        
    };
    Cart.prototype.onMinusButtonClicked = function(event){
        console.log("MinusButton Clicked ...");
        var $event_target = $(event.target);
        var $target_parent = $event_target.parent();
        var itemID = parseInt($target_parent.attr("data-itemid"));
        var price = parseFloat($target_parent.attr("data-price"));
        var quantity = parseInt($(event.target).next().html());
        var $total_price_element = $target_parent.siblings(".cart-item-total-price");
        var $target = $event_target.next();
        var that = this;

        $.ajax({
            type: 'POST',
            url: '/cart/cart_update/',
            data: {product_id: itemID, quantity : quantity - 1},
            dataType:'json',
            success: function(response){
                that.total = response.total;
                that.count = response.count;
                quantity = response.quantity;
                if(quantity == 0){
                   $target_parent.parent().remove();
                }
                else {
                    $target.html(quantity);
                    $total_price_element.html((price * (quantity)) + " FCFA");
                    
                }
                that.notify({});
            },
            error: function(response){
                console.log("Error : couldn't substract the  article");
            }
        });
    };
    Cart.prototype.addObserver = function(observer){
        console.log("Adding Observer ...");
        this.observers.push(observer);
    };
    Cart.prototype.removeObserver = function(observer){
        console.log("Removing Observer ...");
        for(var i = 0; i < this.observers.length; i++){
            if(this.observers[i] === observer){
                this.observers.slice(i, i+1);
                break;
            }
        }
    };
    Cart.prototype.notify = function(item){
        console.log("Notifying Observers ...");
        $(".cart-subtotal").html(this.total + " FCFA");
        
        for (observer in this.observers){
            observer(item);
        }
        this.badgeUpdate();
    };
    Cart.prototype.addItem = function(item){
       
        var that = this;
        // Send request to the Server 
        if(item.is_available != "False"){
            $.ajax({
                type: 'POST',
                url : '/cart/add_to_cart/',
                data: {product_id: item.id, quantity: item.quantity},
                dataType: 'json',
                // success Function called in case of an http 200 response
                success: function(response){
                    that.total = response.total;
                    that.count = response.count;
                    that.notify(item);
                },
                error: function (){
                    alert("Il y a une erreur, Veuillez reessayer.");
                }
            });
        }
       
        else{
            console.log("This article is not available ...");
        }
        
    };
    Cart.prototype.removeItem = function(itemID){
        // Send request to the Server here 
        var index = this.items.findIndex(function(item){
            return item.id === itemID;
        });
        if(index >= 0){
            this.items.slice(index, index);
            this.total -= item.price * item.quantity;
            this.count -= item.quantity;
            this.notify(item);
        }
        
    };
    Cart.prototype.addEventListener = function(event){
        console.log("Adding Event  ... : " +  event.html() );
        this.eventListeners.push(event);
    };
    Cart.prototype.getCount = function(){
        return this.count;
    };
    Cart.prototype.getTotal = function(){
        
        return this.total;
    };

    Cart.prototype.getItem = function(index){
        if(index >= 0 && index < this.count)
            return this.items[index];
        else 
        return {id : -1};
    };

    Cart.prototype.clear = function(){
        while(this.items.length){
            this.items.pop();
        }
        while(this.eventss.length){
            this.events.pop();
        }
        while(this.observers.length){
            this.observers.pop();
        }
        while(this.eventListeners.length){
            this.eventListeners.pop();
        }
        this.total = 0.0;
        this.count = 0;
    };

    Cart.prototype.update = function(req){
        console.log("Update called with itemID : " + req.id + " Qty : " + req.quantity + "\nAction : " +req.action);
    };
    Cart.prototype.badgeUpdate = function(){
        this.eventListeners[0].html("(" + this.count + ")");
    };
    Cart.prototype.getCart = function(){
        var cart = myCart || new Cart();
    };
    return Cart;
})();

var Account = (function(){
    function Account (){
        this.username = "";
        this.email = "";
        this.address1 = "";
        this.address2 = "";
        this.loginState = false;
        this.wishlist = "";
        this.orders = "";


    }

    Account.prototype.init = function(){
        jQuery(".account-Button").click(this.onAccountClicked.bind(this));
        jQuery(".account-Button").hover(this.onAccountHover.bind(this));
        console.log("Account initialized ...");
    };
    Account.prototype.onAccountHover = function(event){
        console.log("AccountButton hovered ...");
        //jQuery(".dropdown-toggle").dropdown();
    };
    Account.prototype.onAccountClicked = function(event){
        console.log("AccountButton clicked ...");
        jQuery(".dropdown-toggle").dropdown();
    };

    return Account ;
})();

//var myCart = new Cart();

Shopping = {};
Shopping.Cart = Cart;
if(typeof (Storage)!== "undefined"){
    shopStorage  = localStorage;
    //shopStorage.Shopping = shopStorage.Shopping || {} ;

    if(shopStorage.Shopping === undefined){
        var store = {'initialized' : 1, 
                     'cartItems' : [],
                     'cartItemCount': 0,
                     'cartTotal' : 0};
        shopStorage.setItem("Shopping", JSON.stringify(store));
    }
    else{
        console.log ("Storage Shopping already initialized : " + shopStorage.Shopping);
    }
    console.log("This Browser support webstorage");
}
else{
    console.log("This Browser doesn't support webstorage");
}
Shopping.myCart = new Shopping.Cart();
Shopping.account = new Account();
Shopping.account.init();
Shopping.myCart.initDefault();
Shopping.myCart.init(jQuery(".cart-badge"));
/*
jQuery(".add-to-cart").click(Shopping.myCart.onAddButtonClicked.bind(Shopping.myCart));
jQuery(".plusButton").click(Shopping.myCart.onPlusButtonClicked.bind(Shopping.myCart));
jQuery(".minusButton").click(Shopping.myCart.onMinusButtonClicked.bind(Shopping.myCart));
jQuery(".removeFromCartButton").click(Shopping.myCart.onRemoveButtonClicked.bind(Shopping.myCart));
jQuery(".cart-popover-button").hover(function(){
    jQuery("#cart-modal").modal({backdrop: false});
});

*/
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

function Observer(observable){
    this.update = function(arg){
        console.log("target has changed ...");
    };
};