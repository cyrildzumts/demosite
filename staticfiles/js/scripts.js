


// display an error message when the
function displayLoginError(){
  $("form.login").submit(function(){
    username = $("#username").val();
    password = $("#password").val();
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
    $(this).find("ul").fadeIn();
    //$(".dropdown-menu").fadeIn("slow");
});
$(".dropdown").mouseleave(function(){
    $(this).find("ul").fadeOut();
    //$(".dropdown-menu").fadeIn("slow");
});

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
        this.$cart_popup                = {};
        this.$cartpopup_content         = {};
        this.events                     = [];
        this.items                      = [];
        this.eventListeners             = [];
        this.$notify_popover            = {}
        this.total                      = 0;
        this.count                      = 0;
        this.userID                     = -1;
        this.observers                  = [];
        this.serverUrl                  = "";
        this.$counter                   = {};
        this.$add_to_cart_btn           = {};
        this.$cart_add_error            = {};
        this.$error_msg                 = {};
    }
    Cart.prototype.initDefault = function(){
        this.$counter = $(".cart-counter");
        this.$cart_add_error = $("#flat-add-error");
        this.$error_msg = $(".flat-error-msg");
        this.$add_to_cart_btn = $("#flat-add-to-cart-btn");
        this.$add_to_cart_btn.click(this.onAddButtonClicked.bind(this));
        $(".add-to-cart").click(this.onAddButtonClicked.bind(this));
        $(".plusButton").click(this.onPlusButtonClicked.bind(this));
        $(".minusButton").click(this.onMinusButtonClicked.bind(this));
        $(".removeFromCartButton").click(this.onRemoveButtonClicked.bind(this));
        //$(".cart-popover-button").hover(function(){
        //$("#cart-modal").modal({backdrop: false});
       // });
       $(".cart-button").hover(this.onCartButtonHover.bind(this), this.onCartButtonHoverLeave.bind(this));
       $(".close-btn").click(this.onCloseBtnClicked.bind(this));
       this.$notify_popover = $("#cart-popover");
       this.$cart_popup = $(".cart-popup");
       this.$cartpopup_content = this.$cart_popup.children(".popup-content");
       console.log("Cart initialised : Cart popup : ");
       console.log(this.$cartpopup_content);
    };
    Cart.prototype.init = function(listener){
        this.addEventListener(listener);
    };
    Cart.prototype.onCloseBtnClicked = function(even){
        console.log("Close Menu btn clicked ...");
        $(".cart-dropdown").toggle();
    };
    Cart.prototype.onCartButtonHover = function(event){
        console.log("Cart hovered ..");
        event.preventDefault();
        //$(".cart-button").dropdown();
    };
    Cart.prototype.onCartButtonHoverLeave = function(event){
        console.log("Cart hovered left..");
        event.preventDefault();
        console.log("Cart contains " + this.count + " article(s)");
        //$(".cart-button").dropdown();
    };
    Cart.prototype.onAddButtonClicked = function(event){
        var item = {};
        item.id = parseInt(this.$add_to_cart_btn.data("itemid"));
        item.is_available = this.$add_to_cart_btn.data("available");
        item.quantity = 1;
        this.addItem(item);
        console.log("Add button clicked ...")
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
        $(".cart-subtotal").html(this.total);
        this.$counter.html(this.count);
        
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
                    that.$error_msg.html("Article ajouté dans le panier.");
                    that.$cart_add_error.toggle().delay(3000).toggle(500);
                    that.notify(item);
                },
                error: function (response){
                    that.$error_msg.html("Une erreur s'est produite, Veuillez reessayer.");
                    that.$cart_add_error.toggle().delay(3000).toggle(500);
                }
            });
        }
       
        else{
            that.$error_msg.html("Cet article n'est plus disponible.");
            that.$cart_add_error.toggle().delay(3000).toggle(500);
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
        var $parent = $(event.target).parent();
        var $qty_target = $parent.children(".item-qty");
        var itemID = parseInt($parent.data("itemid"));
        var price = parseFloat($parent.data("price"));
        var quantity = parseInt($parent.data("quantity"));
        var $root_container = $(`#${itemID}`);
        var $subtotal = $root_container.children(".cart-item-total-price");
        var that = this;
        var requested_qty = -1;
        if(action){
            requested_qty = quantity + 1 ;
        }else{
            requested_qty = quantity - 1;
        }
        $.ajax({
            type: 'POST',
            url: '/cart/cart_update/',
            data: {product_id: itemID, quantity : requested_qty},
            dataType:'json',
            success: function(response){
                that.total = response.total;
                that.count = response.count;
                if(requested_qty == 0){
                    //var querystr = `#${itemID}`;
                    $(`#${itemID}`).remove();
                 }
                 else {
                    $qty_target.html(requested_qty);
                    $parent.data("quantity", requested_qty);
                    $subtotal.html(price * (requested_qty));
                     
                 }
                
                that.notify({});
            },
            error: function(response){
                console.log("Error : l'article n'a pas pu etre actualiser");
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
        $(".account-Button").click(this.onAccountClicked.bind(this));
        $(".account-Button").hover(this.onAccountHover.bind(this));
        console.log("Account initialized ...");
    };
    Account.prototype.onAccountHover = function(event){
        console.log("AccountButton hovered ...");
        //$(".dropdown-toggle").dropdown();
    };
    Account.prototype.onAccountClicked = function(event){
        console.log("AccountButton clicked ...");
        $(".dropdown-toggle").dropdown();
    };

    return Account ;
})();



var Catalog = (function(){
    function Catalog(){
        this.sortOrder          = 1;
        this.CURRENT_SORTING    = 0;
        this.SORTING_PRICE_ASC  = 0;
        this.SORTING_PRICE_DSC  = 1;
        this.SORTING_POPULARITY = 2;
        this.SORTING_RANDOM     = 3;
        this.SORTING_RECENT     = 4;
        this.ordering           = [];
        this.viewedItems        = [];
        this.$items             = {};
        this.$select_filter     = {};
        this.$select_brands     = {};
        this.brands             = [];
        this.brand_filter       = [];
        this.account_menu_popup_is_visible = false;
        this.$category_btn      = {};
        this.$filter_btn        = {};
        this.$clickable         = {};
        this.$close_flat_main   = {};
        this.$brand_input       = {};
        this.$sorting_radios    = {};
        this.$product_list      = {};
        this.$brand_list        = {};
        this.$add_to_cart_btn   = {};
        this.$add_to_wishlist_btn = {};
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

        this.$sorting_radios = $("#flat-sorting-input span input:radio");
        this.$product_list = $("#flat-product-list");
        this.$items = $("#flat-product-list .flat-product");
        this.brands = $("#flat-brands span");
        this.$brand_list = $("#flat-brands span input:checkbox");
        this.$brand_input = $("#brands-filter-input");
        this.$brand_input.keyup(this.onBrandInputChanged.bind(this));
        this.$clickable = $(".flat-clickable");
        this.$close_flat_main = $(".flat-close-main");
        $(".flat-hoverable").hover(function(event){
            event.stopPropagation();
            $(this).children(".flat-product-options").toggle();
            console.log("flat-product hovered");
        });
        this.$clickable.click(function(event){
            event.stopPropagation();
            console.log("Clickable clicked ...");
            $(this).siblings(".flat-main-content").toggle();
        });
        this.$close_flat_main.click(function(event){
            event.stopPropagation();
            $(this).parents(".flat-main-content").hide();
        });
        this.$category_btn = $(".flat-cat-close");
        this.$filter_btn = $(".flat-filter-close");
        /* this.$filter_btn.click(function(event){
            event.stopPropagation();
            console.log("filter close drop clicked ");
            $(this).parents(".flat-dropdown-wrapper").toggle();
        });
        this.$category_btn.click(function(event){
            event.stopPropagation();
            console.log("cat close drop clicked ");
            $(this).parents(".flat-dropdown-wrapper").toggle();
        }); */
        // Dropdown Account Menu 
        $(".flat-account-dropdown-btn").click(function(event){
            event.stopPropagation();
            console.log("Account icon clicked ...");
            $(".flat-account-drop-wrapper").toggle();
            console.log($(event.target));
        });
        $(".flat-cancel-btn").click(function(event){
            event.stopPropagation();
            $( ".flat-account-drop-wrapper, .flat-dropdown-wrapper").
            each(function(index, element){
                if($(element).css("display") !== "none"){
                    $(element).hide();
                }
            });
        });
        /**
         * Controls click event emitted from the Flat Account Menu
         * contained in a flat-account-drop-wrapper or flat-dropdown-wrapper
         */
        $(".flat-dropdown-btn").click(function(event){
            event.stopPropagation();
            console.log("drop clicked ");
            $(this).siblings(".flat-dropdown-wrapper").toggle();
        });
        
        /**
         * Controls click on the flat nav menu.
         * This element contains the side site menu
         */
        $(".flat-nav-menu").click(function(event){
            event.stopPropagation();
            $("#flat-site-menu").toggle();
            console.log("menu clicked ...")
        });
        $(".flat-btn-menu-close").click(function(event){
            event.stopPropagation();
            $("#flat-site-menu").hide();
            console.log("menu clicked ...")
        });

        this.getItems();
        $("#flat-filter-apply").click(this.onFilterChanged.bind(this));
        $("#btn-filter-reset").click(this.onFilterReset.bind(this));
        $("#flat-sort-apply").click(this.onSortingChanged.bind(this));
        $("#btn-sort-reset").click(this.onSortingReset.bind(this));
        this.$select_filter = $("#select-filter");
        this.$select_brands = $("#select-brands");
        for(var i = 0; i < this.brands.length; i++){
            this.$select_brands.append(`<input  type="checkbox" value=${i}> <span class="brand-entry"> ${this.brands[i]} </span>`); 
        }
    };
    Catalog.prototype.onBrandInputChanged = function(event){
        var val = this.$brand_input.val().toLowerCase();
        this.brands.filter(function(i, e){
            $(e).toggle($(e).text().toLowerCase().indexOf(val) > -1)
        });
        console.log("Brands input changed ...");
    };
    Catalog.prototype.onFilterChanged = function(event){
        //this.$select_filter.collapse("toggle");
        var $selected_brands = this.$brand_list.filter(":checked");
        console.log("Filter Selected : " );
        console.log($selected_brands);
        /* for(var i = 0; i < this.$brand_list.length; i++){
            console.log(this.brands[$input[i].value]);
            console.log("--------------");
            this.brand_filter.push(this.brands[$input[i].value]);
        }
         */
        that = this;
        var sel = {};
        var element = {};
        var match = false;
        if($selected_brands.length > 0){
            this.$items.each(function(i, e){
                element = $(e);
                $selected_brands.each(function(j,input){
                    sel = $(input).val();
                    console.log("Look for items to mask");
                    console.log("Brand : " + sel);
                    console.log("Item being checked " );
                    console.log(element);
                    console.log("Element Brand : " + element.data("brand"));
                    if(sel == $(e).data("brand")){
                        match = true;
                    }
                });
                if(match){
                    element.show();
                    match = false;
                }
                else{
                    element.hide();
                }
            });
        }
        else {
            this.$items.each(function(i, e){
                $(e).show();
            });
        } 
    };

    Catalog.prototype.onSortingChanged = function(event){
        event.stopPropagation();
        event.preventDefault();
        var order = this.$sorting_radios.filter(":checked").val();
        order = parseInt(order);
        console.log("Sorting changed to " + this.ordering[order]);
        this.sort(order);
        this.$product_list.empty();
        this.$items.appendTo(this.$product_list);

    };
    Catalog.prototype.onSortingReset = function(event){
        event.preventDefault();
        console.log("Sorting reset");
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
    Catalog.prototype.sortByPrice = function(order){
        var key = "price";
        if(order == this.SORTING_PRICE_DSC){
            this.$items.sort(function(a, b){
                return $(b).data(key) - $(a).data(key);
            });
        }
        else if(order == this.SORTING_PRICE_ASC){
            this.$items.sort(function(a, b){
                return $(a).data(key) - $(b).data(key);
            });
        }
    };
    Catalog.prototype.sortByPopularity = function(key){
        this.$items.sort(function(a, b){
            return $(b).data(key) - $(a).data(key);
        });
    };
    Catalog.prototype.sort = function(sortType){
        console.log(" sort () : This method is not implemented yet ...");
        var key = "";
        switch (sortType) {
            case this.SORTING_PRICE_DSC:
            case this.SORTING_PRICE_ASC:
                this.sortByPrice(sortType);
                break;
            case this.SORTING_POPULARITY:
                this.sortByPopularity("viewcount");
                break;
            case this.SORTING_RANDOM:

                break;
            case this.SORTING_RECENT:

                break;
        
            default:
                break;
        }
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
        
        console.log(this.$items);
        console.log("We found " + this.$items.length + " in this page");

    };
    Catalog.prototype.getBrands = function (){
        console.log("getBrands() called ...");
    };
    return Catalog;
})();
//var myCart = new Cart();

var Wishlist = (function(){
    function Wishlist(){
        this.items = [];
        this.count = 0;
        this.$bagde = {};
        this.$counter = {};
        this.$error_msg = {};

    }
    Wishlist.prototype.init = function(){
        this.$error_msg = $(".flat-error-msg");
        this.$bagde = $(".wishlist-badge");
        this.$counter = $(".wishlist-counter");
        $(".add-to-wishlist").click(this.onAddButtonClicked.bind(this));
        $("#flat-add-to-wishlist-btn").click(this.onAddButtonClicked.bind(this));
        $(".wishlist-remove").click(this.onRemoveButtonClicked.bind(this));
        $(".wishlist-clear").click(this.onClearButtonClicked.bind(this));
    }
    Wishlist.prototype.onAddButtonClicked = function(event){
        var item = {};
        var $target = $(event.target);
        var $element = $(event.target).parent();
        item.id = parseInt($element.data("itemid"));
        item.name = $element.data("name");
        //item.image = $element.data("image");
        console.log("attr itemid : " + item.id);
        console.log("Item to add into wishlist : \nName : " + item.name);
        this.addItem(item);
        
    };
    Wishlist.prototype.onRemoveButtonClicked = function(event){
        var item = {};
        var $target = $(event.target);
        var $element_to_remove = $target.parent();
        item.id = parseInt($element_to_remove.attr("data-itemid"));
        item.name = $element_to_remove.attr("data-name");
        item.image = $element_to_remove.attr("data-image");
        console.log("Item to Remove : \nName : " + item.name);
        this.removeItem(item.id);
        
    };
    Wishlist.prototype.onClearButtonClicked = function(event){
        var item = {};
        var $target = $(event.target);
        var $element_to_remove = $target.parent();
        this.clear();
    };
    Wishlist.prototype.addItem = function(item){
        var that = this;
        var notification = {};
        $.ajax({
            type: 'POST',
            url: '/wishlist/ajax_add_to_wishlist/',
            data: {product_id: item.id},
            dataType:'json',
            success: function(response){
                console.log("Wishlist : Add request sent successfully");
                that.count =  response.item_count;
                notification.added = true;
                notification.message = "L'article a été ajouter \nà votre liste de souhait";
                that.notify(notification);
            },
            error: function(response){
                console.log("Error : couldn't add item into the wishlist");
                notification.added = false;
                notification.message = "L'article n'a pas pu être ajouté à votre liste de souhait";
                that.notify(notification);
            }
        });
        
        
    };
    Wishlist.prototype.removeItem = function(itemID){
        var that = this;
        $.ajax({
            type: 'POST',
            url: '/wishlist/ajax_remove_from_wishlist/',
            data: {product_id: itemID},
            dataType:'json',
            success: function(response){
                console.log("Wishlist : Remove request sent successfully");
                that.count =  response.item_count;
                $(`#${itemID}`).remove();
                that.notify({});
            },
            error: function(response){
                console.log("Error : couldn't remove item from the wishlist");
            }
        });
    };
    Wishlist.prototype.clear = function(){
        var that = this;
        $.ajax({
            type: 'POST',
            url: '/wishlist/ajax_wishlist_clear/',
            data: {},
            dataType:'json',
            success: function(response){
                console.log("Clear request sent successfully");
                console.log("Wishlist cleared : " +  response.state);
                that.count =  response.item_count;
                that.notify({});
            },
            error: function(response){
                console.log("Error : couldn't remove item from the wishlist");
            }
        });
        
    };

    Wishlist.prototype.get = function(itemID){
        return this.items.find(function(item){
            return item.id === itemID;
        });
    };

    Wishlist.prototype.notify = function(notification){
        console.log("Wishlist changed ...");
        this.$error_msg.html(notification.message);

        this.$counter.html("<strong>" + this.count + " </strong>");
        this.$error_msg.parent().toggle().delay(3000).toggle(500);

        //location.reload(true);
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
Shopping.myCart.init($(".cart-badge"));
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