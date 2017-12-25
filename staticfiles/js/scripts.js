

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
        this.update(event, true);
    };
    Cart.prototype.onMinusButtonClicked = function(event){
        console.log("MinusButton Clicked ...");
        this.update(event, false);
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
        $(".cart-subtotal").html("<strong>" + this.total + " FCFA" +  "</strong>");
        
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

    Cart.prototype.update = function(event, action){
        var $target = $(event.target);
        var $quantity_target = $target.siblings(".cartItem-qty");
        var itemID = parseInt($target.parent().attr("data-itemid"));
        var price = parseFloat($target.parent().attr("data-price"));
        var quantity = parseInt($quantity_target.html());
        var $span = $target.parent().siblings(".cart-item-total-price").find("span");
        var that = this;
        var requested_qty = action ? quantity + 1 : quantity - 1;
        $.ajax({
            type: 'POST',
            url: '/cart/cart_update/',
            data: {product_id: itemID, quantity : requested_qty},
            dataType:'json',
            success: function(response){
                that.total = response.total;
                that.count = response.count;
                if(requested_qty == 0){
                    $target.parent().parent().parent().remove();
                 }
                 else {
                    $quantity_target.html(requested_qty);
                    $span.html("<strong> Total : " + (price * (requested_qty)) + " FCFA" + "</strong>");
                     
                 }
                
                that.notify({});
            },
            error: function(response){
                console.log("Error : couldn't update article");
            }
        });
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

var Wishlist = (function(){
    function Wishlist(){
        this.items = [];
        this.$bagde = {};

    }
    Wishlist.prototype.init = function(){
        this.$bagde = $(".wishlist-badge");
        $(".wishlist-add-btn").click(this.onAddButtonClicked.bind(this));
        $(".wishlist-remove-btn").click(this.onRemoveButtonClicked.bind(this));
        $(".wishlist-clear-btn").click(this.onClearButtonClicked.bind(this));
    }
    Wishlist.prototype.onAddButtonClicked = function(event){
        var item = {};
        var $target = $(event.target);
        var $element_to_remove = $target.parent();
        item.id = parseInt($element_to_remove.attr("data-itemID"));
        item.name = $element_to_remove.attr("data-name");
        item.image = $element_to_remove.attr("data-image");
        console.log("Item to Remove : \nName : " + item.name + "\nImage : " + item.image);
        this.addItem(item);
        
    };
    Wishlist.prototype.onRemoveButtonClicked = function(event){
        var item = {};
        var $target = $(event.target);
        var $element_to_remove = $target.parent();
        item.id = parseInt($element_to_remove.attr("data-itemID"));
        item.name = $element_to_remove.attr("data-name");
        item.image = $element_to_remove.attr("data-image");
        console.log("Item to Remove : \nName : " + item.name + "\nImage : " + item.image);
        this.removeItem(item.id);
        
    };
    Wishlist.prototype.onClearButtonClicked = function(event){
        var item = {};
        var $target = $(event.target);
        var $element_to_remove = $target.parent();
        this.clear();
    };
    Wishlist.prototype.addItem = function(item){
        var $target = $(event.target);
        var that = this;
        $.ajax({
            type: 'POST',
            url: '/wishlist/ajax_add_to_wishlist/',
            data: {product_id: itemID},
            dataType:'json',
            success: function(response){
                console.log("Add request sent successfully");
                console.log("Item added : " +  response.state);
                console.log("Item Count   : " +  response.item_count);
                //$(`#${itemID}`).remove();
                that.notify({});
            },
            error: function(response){
                console.log("Error : couldn't add item into the wishlist");
            }
        });
        
        this.notify();
        
    };
    Wishlist.prototype.removeItem = function(itemID){
        var $target = $(event.target);
        var that = this;
        $.ajax({
            type: 'POST',
            url: '/wishlist/ajax_remove_from_wishlist/',
            data: {product_id: itemID},
            dataType:'json',
            success: function(response){
                console.log("Remove request sent successfully");
                console.log("Item removed : " +  response.state);
                console.log("Item Count   : " +  response.item_count);
                $(`#${itemID}`).remove();
                that.notify({});
            },
            error: function(response){
                console.log("Error : couldn't remove item from the wishlist");
            }
        });
        
        this.notify();
    };
    Wishlist.prototype.clear = function(){

        this.notify();
    };

    Wishlist.prototype.get = function(itemID){
        return this.items.find(function(item){
            return item.id === itemID;
        });
    };

    Wishlist.prototype.notify = function(){
        console.log("Wishlist changed ...");
    };

    return Wishlist;
})();


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
Shopping.wishlist =  new Wishlist();
Shopping.catalog.init(0);
Shopping.account.init();
Shopping.myCart.initDefault();
Shopping.myCart.init(jQuery(".cart-badge"));
Shopping.wishlist.init();

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