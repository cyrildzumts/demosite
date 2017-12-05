

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
       jQuery(".close-btn").click(this.onCloseBtnClicked.bind(this));
    };
    Cart.prototype.init = function(listener){
        this.addEventListener(listener);
    };
    Cart.prototype.onCloseBtnClicked = function(even){
        console.log("Close Menu btn clicked ...");
        jQuery(".cart-dropdown").toggle();
    };
    Cart.prototype.onCartButtonHover = function(event){
        console.log("Cart hovered ..");
        //$(".cart-button").dropdown();
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



var Catalog = (function(){
    function Catalog(){
        this.sortOrder         = 1;
        this.CURRENT_SORTING    = 0;
        this.SORTING_PRICE_ASC  = 1;
        this.SORTING_PRICE_DSC  = 2;
        this.SORTING_POPULARITY = 3;
        this.SORTING_RANDOM     = 4;
        this.ordering           = [];
        this.viewedItems       = [];
        this.$items             = {};
        this.$select_filter    = {};
        this.$select_brands    = {};
        this.brands            = [];
        this.brand_filter      = [];
    }
    Catalog.prototype.init = function(sorting){
        this.ordering[0]                         = "NO ACTIV SORTING ";
        this.ordering[this.SORTING_PRICE_ASC]     = "ASCENDING SORTING";
        this.ordering[this.SORTING_PRICE_DSC]     = "DESCENDING SORTING";
        this.ordering[this.SORTING_POPULARITY]    = "POPULARITY SORTING";
        this.ordering[this.SORTING_RANDOM]        = "RANDOM SORTING";
        if((sorting >= 0) && (sorting <= this.SORTING_RANDOM)){
            this.CURRENT_SORTING = sorting;
            this.filter();
        }
        this.getItems();
        $("#btn-filter").click(this.onFilterChanged.bind(this));
        $("#btn-filter-reset").click(this.onFilterReset.bind(this));
        this.$select_filter = $("#select-filter");
        this.$select_brands = $("#select-brands");
        for(var i = 0; i < this.brands.length; i++){
            this.$select_brands.append(`<input  type="checkbox" value=${i}> <span class="brand-entry"> ${this.brands[i]} </span>`); 
        }
    };
    Catalog.prototype.onFilterChanged = function(event){
        this.$select_filter.collapse("toggle");
        var $input = $("#select-brands input:checked");
        console.log("Filter Selected : " );
        for(var i = 0; i < $input.length; i++){
            console.log(this.brands[$input[i].value]);
            console.log("--------------");
            this.brand_filter.push(this.brands[$input[i].value]);
        }
        
        this.filter();
    };

    Catalog.prototype.onSortingChanged = function(event){
        console.log("Sorting changed to " + this.ordering[this.CURRENT_SORTING]);
    };
    Catalog.prototype.onFilterReset = function(event){
        event.preventDefault();
        console.log("Reset pressed...");
        
        $('#select-brands input:checkbox').prop('checked', false);
        this.$items.show();

    };
    Catalog.prototype.filter = function(){
        console.log(" filter () : This method is not implemented yet ...");
        for(var i = 0; i < this.$items.length; i++){
            if(this.brand_filter.includes($(this.$items[i]).attr("data-brand"))){
                $(this.$items[i]).hide();
            }
            else{
                $(this.$items[i]).show();
            }
        }
        this.brand_filter_clear();
        
    };
    Catalog.prototype.brand_filter_clear = function(){
        while(this.brand_filter.length){
            this.brand_filter.pop();
        }
    };
    Catalog.prototype.sort = function(){
        console.log(" sort () : This method is not implemented yet ...");
    };
    Catalog.prototype.search = function(){
        console.log(" search () : This method is not implemented yet ...");
    };
    Catalog.prototype.onSearchInputChanged = function(query){
        console.log(" Searched Query : " + query);
    };
    Catalog.prototype.renderViewedItems = function(){
        console.log(" render () : This method is not implemented yet ...");
    };

    Catalog.prototype.getItems = function(){
        console.log(" getItems () : This method is not implemented yet ...");
        this.$items = $("#product-list .list-entry");
        console.log("We found " + this.$items.length + " in this page");
        this.getBrands();

    };
    Catalog.prototype.getBrands = function (){
        var brand ;
        for (var i = 0; i < this.$items.length; i++){
            brand = $(this.$items[i]).attr("data-brand");
            if (!this.brands.includes(brand)){
                this.brands.push(brand);
            }
        }
    };
    return Catalog;
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
Shopping.myCart  = new Shopping.Cart();
Shopping.account = new Account();
Shopping.catalog = new Catalog();
Shopping.catalog.init(0);
Shopping.account.init();
Shopping.myCart.initDefault();
Shopping.myCart.init(jQuery(".cart-badge"));

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