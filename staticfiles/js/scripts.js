


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



var Collapsible = (function(){
    function Collapsible(){
        this.$collapsible   = {}; // all element with collapsible class
        this.$close         = {}; // all button used to close a collapsible elements.

    }
    Collapsible.prototype.init = function(){
        console.log("Initializing Collapsible ...")
        this.$collapsible = $(".collapsible");
        this.$close = this.$collapsible.children(".close");
        console.log("Found " + this.$collapsible.length + " collapsibles on this pages.");
        console.log("Found " + this.$close.length + " collapsibles closes on this pages.");
        this.$collapsible.children(".open").click(function(event){
            event.stopPropagation();
            var target =$(event.target).data("target");
            if(target == undefined){
                $(this).parent().children("ul").toggle();
            }
            else{
                $(target).toggle();
                console.log("Target : " + target);
            }
            
            
        });
        this.$close.click(function(event){
            console.log("collapsible closing ...");
            event.stopPropagation();
            var target =$(event.target).data("target");
            $(target).toggle();
        });
    };

    return Collapsible;
})();

var Modal = (function(){
    function Modal(){
        this.$modal         = {};
        this.$accountModal  = {};
        this.$cartModal     = {};
        this.$wishlistModal = {};
        this.$editModal     = {};
        this.$checkoutModal = {};
        this.$filterModal   = {};
        this.$sortOrderModal= {};
        this.$openModal     = {};
        this.$closeModal    = {};

    };

    Modal.prototype.init = function(){
        console.log("Modal plugin initialization ...");
        this.$accountModal  = $("#account-modal");
        this.$cartModal     = $("#cart-modal");
        this.$wishlistModal = $("#wishlist-modal");
        this.$editModal     = $(".edit-modal");
        this.$checkoutModal = $("#checkout-modal");
        this.$filterModal   = $("#filter-modal");
        this.$sortOrderModal= $("#sortOrder-modal");
        this.$openModal     = $(".flat-open-modal");
        this.$closeModal    = $(".flat-close-modal");
        
        that = this;
        this.$openModal.click(function(event){
            event.stopPropagation();
            that.$modal = $($(this).data('target'));
            that.$modal.show();
            
        });
        $(window).click(function(event){
            var $target = $(event.target);
            console.log("window click event fired ...");
            console.log("modal : ");
            console.log(that.$modal);
            console.log("event target : ");
            console.log($target);
            if($target.is(that.$modal)){
                console.log("modal clicked");
                that.$modal.hide();
            }
            
        });
        this.$closeModal.click(function(event){
            //that.$modal = $($(this).data('target'));
            that.$modal.toggle();
        });
        
        console.log("Modal plugin installed ...");
    };


    return Modal;
})();

var Tabs = (function(){
    function Tabs(){
        this.currentTab     = 0;
        this.tabCount       = 0;
        this.tabs           = {};
        this.tab            = {};
        this.tabsCount      = 0;
        
    };

    Tabs.prototype.init = function(){
        this.tabsCount = $(".flat-tabs").length;
        this.tabs = $(".flat-tabcontent");
        this.tab = $(".flat-tab");
        this.tabCount = this.tab.length;
        this.tab.click(this.onTabClicked.bind(this));
        this.tabs.hide();
        this.update();
        console.log("Tabs suceesfully initialized :");
        console.log(" Tabs found " + this.tabCount + " on this page");
        console.log("there are " + this.tabsCount + " tabs on this page");
    };
    Tabs.prototype.onTabClicked = function(event){
        var tab = parseInt($(event.target).data("index"));
        if(tab != this.currentTab){
            console.log("Tabs Plugin : Tab Clicked");
            this.currentTab = tab;
                this.update();
        }
    };
    Tabs.prototype.update = function(){
        this.tab.removeClass("active");
        $(this.tab[this.currentTab]).addClass("active");
        var that = this;
        this.tabs.hide();
        $(this.tabs[this.currentTab]).show();
    };
    return Tabs;
})();

var Cart = (function(){
    function Cart(){

        this.events                     = [];
        this.items                      = [];
        this.eventListeners             = [];
        this.total                      = 0;
        this.count                      = 0;
        this.userID                     = -1;
        this.observers                  = [];
        this.serverUrl                  = "";
        this.$counter                   = {};
        this.$add_to_cart_btn           = {};
        this.catalog                    = {};
        this.$add_to_wishlist_btn       = {};
        this.$checkout_link             = {};
        this.$summary                   = {};
    }
    Cart.prototype.init = function(){
        this.$summary = $("#js-cart-summary");
        this.$add_to_wishlist_btn = $(".js-cart-add-to-wishlist");
        this.$add_to_wishlist_btn.click(this.onAddToWishlistClicked.bind(this));
        this.$checkout_link = $(".flat-checkout-link");
        this.$counter = $(".cart-counter");
        this.$add_to_cart_btn = $("#flat-add-to-cart-btn");
        this.$add_to_cart_btn.click(this.onAddButtonClicked.bind(this));
        $("#js-add-to-cart").click(this.onAddButtonClicked.bind(this));
        $(".js-cart-item-up").click(this.onPlusButtonClicked.bind(this));
        $(".js-cart-item-down").click(this.onMinusButtonClicked.bind(this));
        $(".js-cart-remove").click(this.onRemoveButtonClicked.bind(this));
        //$(".cart-popover-button").hover(function(){
        //$("#cart-modal").modal({backdrop: false});
       // });
       //$(".cart-button").hover(this.onCartButtonHover.bind(this), this.onCartButtonHoverLeave.bind(this));
       //$(".close-btn").click(this.onCloseBtnClicked.bind(this));
    };
    Cart.prototype.addCatalog = function(catalog){
        this.catalog = catalog;
        this.catalog.setCart(this);
    }
    Cart.prototype.onCloseBtnClicked = function(even){
        event.stopPropagation();
        console.log("Close Menu btn clicked ...");
        $(".cart-dropdown").toggle();
    };
    Cart.prototype.onCartButtonHover = function(event){
        event.stopPropagation();
        console.log("Cart hovered ..");
        event.preventDefault();
        //$(".cart-button").dropdown();
    };
    Cart.prototype.onCartButtonHoverLeave = function(event){
        event.stopPropagation();
        console.log("Cart hovered left..");
        event.preventDefault();
        console.log("Cart contains " + this.count + " article(s)");
        //$(".cart-button").dropdown();
    };
    Cart.prototype.onAddToWishlistClicked = function(event){
        event.stopPropagation();
        console.log("Cart : moving item to Wishlist");
        var item = {};
        var $target = $($(event.target).data('target'));
        item.id = $target.data("product-id");
        if(isNaN(item.id)){
            console.log("Item ID is NaN");
            this.catalog.notify({message: "ID non identifié. Si le problème persiste veuillez nous contatcter. "});
        }
        else{
            this.catalog.addToWishlist(item);
        }
        
    }
    Cart.prototype.onAddButtonClicked = function(event){
        event.stopPropagation();
        var item = {};
        var $target = $($(event.target).data("target"));
        item.id = parseInt($target.data("product-id"));
        item.is_available = $target.data("available");
        item.quantity = 1;
        this.addItem(item);
    };
    Cart.prototype.onRemoveButtonClicked = function(event){
        event.stopPropagation();
        var $target = $($(event.target).data("target"));
        var itemID = parseInt($target.data("product-id"));
        var that = this;
        console.log("Cart Remove : ID = " + itemID);
        $.ajax({
            type: 'POST',
            url: '/cart/cart_update/',
            data: {product_id: itemID, quantity : 0},
            dataType:'json',
            success: function(response){
                that.total = response.total;
                that.count = response.count;
                $target.remove();
                that.notify({});
                that.catalog.notify({message: "L'article a été retiré du Panier"});
            },
            error: function(response){
                that.catalog.notify({message: "L'article n'a pas pû être retiré du Panier"});
                console.log("Error : couldn't remove the  article");
            }
        });
    };
    Cart.prototype.onPlusButtonClicked = function(event){
        event.stopPropagation();
        console.log("PlusButton Clicked ...  : ");
        this.update(event, true);
    };
    Cart.prototype.onMinusButtonClicked = function(event){
        event.stopPropagation();
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
        if(this.count == 0){
            this.$checkout_link.hide();
            this.$summary.hide();
        }
        else{
            this.$checkout_link.show();
            this.$summary.show();
        }
        this.badgeUpdate();
    };
    Cart.prototype.addItem = function(item){
       
        var that = this;
        // Send request to the Server 
        if(item.is_available == "True"){
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
                    that.catalog.notify({message: "L'article a été ajouté dans le Panier"});
                },
                error: function (response){
                    this.catalog.notify({message: "L'article n'a pas pu être ajouté dans le Panier"});
                }
            });
        }
       
        else{
            that.catalog.notify({message: "Cet article n'est plus disponible."});
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
         var notification = {};
        var $target = $($(event.target).data("target"));
        var $qty_target = $(event.target).siblings(".product-quantity");
        var itemID = parseInt($target.data("product-id"));
        var price = parseFloat($target.data("price"));
        var quantity = parseInt($target.data("quantity"));
        
        var $subtotal = $target.find(".product-price-total");
        console.log("Cart update : ");
        console.log($subtotal);
        var that = this;
        var requested_qty = -1;
        if(action){
            requested_qty = quantity + 1 ;
        }else{
            requested_qty = quantity - 1;
        }
        console.log("Cart quantity update : " + requested_qty);
        console.log($qty_target);
        $.ajax({
            type: 'POST',
            url: '/cart/cart_update/',
            data: {product_id: itemID, quantity : requested_qty},
            dataType:'json',
            success: function(response){
                that.total = response.total;
                that.count = response.count;
                if(response.updated){
                   if(response.quantity > 0){
                    $qty_target.html(response.quantity);
                    $target.data("quantity", response.quantity);
                    $subtotal.html(price * (response.quantity));
                    
                   }
                   else{
                    $target.remove();
                   }
                   notification.message= "Le Panier a été actualisé";
                }
                else{
                    if(response.quantity_error){
                        notification.message= "Vous avez atteint la quantité maximale pour cet article";
                    }
                    else{
                        notification.message= "Il a eu une erreur interne. veuillez reéssayer plus tard";
                    }
                }
               
                that.notify({});
                that.catalog.notify(notification);
                
            },
            error: function(response){
                that.catalog.notify({message: "Le Panier n'a pas pu être actualisé"});
                console.log("Error : l'article n'a pas pu etre actualiser");
            }
        });
    };
    Cart.prototype.badgeUpdate = function(){

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
        this.cart               = {};
        this.wishlist           = {};
        this.$canvamenu          = {};
        this.$site_wrapper      = {};
        this.$canva_menu_btn    = {};
        this.$canva_container   = {};
        this.$notification      = {};
        this.$notification_content = {};
        this.timeoutID          = -1;
    }
    Catalog.prototype.init = function(sorting){
        var that = this;
        this.ordering[0]                         = "NO ACTIV SORTING ";
        this.ordering[this.SORTING_PRICE_ASC]     = "ASCENDING SORTING";
        this.ordering[this.SORTING_PRICE_DSC]     = "DESCENDING SORTING";
        this.ordering[this.SORTING_POPULARITY]    = "POPULARITY SORTING";
        this.ordering[this.SORTING_RANDOM]        = "RANDOM SORTING";
        if((sorting >= 0) && (sorting <= this.SORTING_RANDOM)){
            this.CURRENT_SORTING = sorting;
            this.filter();
        }
        this.$notification = $("#notification");
        this.$notification_content = this.$notification.children(".content");
        this.$canva_menu_btn = $("#js-canva-menu");
        this.$canvamenu = $("#site-canva-menu");
        this.$canva_container = this.$canvamenu.children(".canva-container");
        this.$site_wrapper= $("#site-wrapper");
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
        $(".js-notify-close").click(function(event){
            event.stopPropagation();
            console.log("closing notification...");
            if(that.timeoutID > 0){
                console.log("A timer is active : timer ID = " + that.timeoutID);
                clearTimeout(that.timeoutID);
                that.timeoutID = -1;
            }
            that.$notification.hide();

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

        /**
         * OFF-CANVA-MENU
         */
         $("#js-canva-menu").click(function(event){
             console.log("click on canva button");
            var left = that.$canvamenu.css("left");
            console.log("click on canva button");
            console.log("canva menu  LEFT Property : " +  left);
            if (left == "0px"){
                that.$canvamenu.css("left", "-200px");
                that.$site_wrapper.css("margin-left", "0");
            }
            else if (left == "-200px"){
                that.$canvamenu.css("left", "0");
                that.$site_wrapper.css("margin-left", "200px");
            }
         });

         $(".js-close-canva").click(function(event){
            var target = $($(".js-close-canva").data("target"));
            target.css("left", "-200px");
            that.$site_wrapper.css("margin-left", "0");
            $(".collapsible ul").hide();
         });
         

    };

    Catalog.prototype.setCart = function(cart){
        console.log("Catalog adding Cart instance ");
        this.cart = cart;
    };
    Catalog.prototype.setWishlist = function(wishlist){
        console.log("Catalog adding Wishlist instance ");
        this.wishlist = wishlist;
    };


    Catalog.prototype.addToCart = function(item){
        this.cart.addItem(item);
    };
    Catalog.prototype.addToWishlist = function(item){
        this.wishlist.addItem(item);
    }

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

    Catalog.prototype.notify = function(notification){
        var that = this;
        if(notification.message != "undefined"){
            this.$notification_content.html(notification.message); 
        }
        else{
            console.log("Bad notification object");
            this.$notification_content.html("Erreur du format de notifition"); 
        }

        this.$notification.show("slow", function(){
            var element = this;
            that.timeoutID = setTimeout(function(){
                $(element).hide();
                //that.timeoutID = -1;
            }, 5000);
            console.log("timerID : " + that.timeoutID);
        });
    };
    return Catalog;
})();
//var myCart = new Cart();

var Wishlist = (function(){
    function Wishlist(){
        this.items              = [];
        this.count              = 0;
        this.$bagde             = {};
        this.$counter           = {};
        this.catalog            = {};
        this.$add_to_cart_btn   = {};
        this.$clear_btn         = {};

    }
    Wishlist.prototype.init = function(){
        this.$clear_btn = $(".js-wishlist-clear");
        this.$bagde = $(".wishlist-badge");
        this.$counter = $(".js-wishlist-counter");
        this.$add_to_cart_btn = $(".js-move-to-cart");
        this.$add_to_cart_btn.click(this.onAddToCartClicked.bind(this));
        $("#js-add-to-wishlist").click(this.onAddButtonClicked.bind(this));
        $("#flat-add-to-wishlist-btn").click(this.onAddButtonClicked.bind(this));
        $(".js-remove-from-wishlist").click(this.onRemoveButtonClicked.bind(this));
        this.$clear_btn.click(this.onClearButtonClicked.bind(this));
    }
    Wishlist.prototype.addCatalog = function(catalog){
        this.catalog = catalog;
        this.catalog.setWishlist(this);
    }

    Wishlist.prototype.onAddToCartClicked = function(event){
        event.stopPropagation();
        console.log("Wishlist : moving item to Cart");
        var item = {};
        var $target = $($(event.target).data("target"));
        item.id = parseInt($target.data("product-id"));
        item.is_available = $target.data("available");
        item.quantity = 1;
        this.catalog.addToCart(item);
    }
    Wishlist.prototype.onAddButtonClicked = function(event){
        event.stopPropagation();
        console.log("Add to wishlist : " );
        
        var item = {};
        var $target = $($(event.target).data("target"));
        console.log($target);
        item.id = parseInt($target.data("product-id"));
        
        if(!isNaN(item.id)){
            this.addItem(item);
        }
        else{
            console.log("Item has an invalid ID : " + item.id);
        }
        
    };
    Wishlist.prototype.onRemoveButtonClicked = function(event){
        event.stopPropagation();
        var item = {};
        var target_id = $(event.target).data("target");
        var $target = $(target_id);
        console.log("Removing WI : " +  target_id);
        item.id = parseInt($target.data("itemid"));
        this.removeItem(item.id, $target);
        
    };
    Wishlist.prototype.onClearButtonClicked = function(event){
        event.stopPropagation();
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
                notification.added = response.added;
                console.log("Response Added : " + response.added);
                console.log("Response Duplicate : " + response.duplicated);
                if(response.added){
                    notification.message = "L'article a été ajouté à vos Favoris";
                }
                else{
                    if (response.duplicated){
                        notification.message = "Cet article est déjà dans vos Favoris";
                    }
                }
                
                that.notify(notification);
            },
            error: function(response){
                console.log("Error : couldn't add item into the wishlist");
                notification.added = false;
                notification.message = "L'article n'a pas pu être ajouté à vos Favoris";
                that.notify(notification);
            }
        });
        
        
    };
    Wishlist.prototype.removeItem = function(itemID, $element_to_remove){
        var that = this;
        $.ajax({
            type: 'POST',
            url: '/wishlist/ajax_remove_from_wishlist/',
            data: {product_id: itemID},
            dataType:'json',
            success: function(response){
                console.log("Wishlist : Remove request sent successfully");
                that.count =  response.item_count;
                $element_to_remove.remove();
                that.notify({message: "L'article a été retiré des Favoris"});
            },
            error: function(response){
                that.notify({message: "L'article n'a pas pu être retiré des Favoris"});
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
                $("#wishlist .content").children().remove();
                that.notify({message: "La liste des Favoris a été vidée"});
            },
            error: function(response){
                that.notify({message: "Erreur : La Liste des Favoris n'a pas pu être vidée"});
                console.log("Error : couldn't clear the wishlist");
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
        this.$counter.html("<strong>" + this.count + " </strong>");
        if(this.count == 0){
            this.$clear_btn.hide();
        }
        else{
            this.$clear_btn.show();
        }
        this.catalog.notify(notification);
        
    };

    return Wishlist;
})();


var Checkout = (function(){
    function Checkout(){
        this.currentTab = 0;
        this.tabCount = 0;
        this.tabs = {};
        this.tab = {};
        this.nextBtn = {};
        this.prevBtn = {};
        this.submitBtn = {};
        this.paiementChoiceBtn = {};
        this.$inputs = {};
        this.$form = {};

    }
    Checkout.prototype.init = function(){
        this.paiementOpt = 2;
        this.$form = $("#flat-order-form");
        this.tabs = $(".flat-tabcontent-checkout");
        this.tab = $(".flat-tab-checkout");
        this.nextBtn = $("#js-checkout-next-btn");
        this.prevBtn = $("#js-checkout-prev-btn");
        this.submitBtn = $("#js-checkout-submit-btn");
        this.paiementChoiceBtn = $(".choice");
        this.$inputs = this.paiementChoiceBtn.find('[type="radio"]');
        console.log("Checkout Init : we found " + this.$inputs.length + " inputs");
        this.prevBtn.hide();
        this.tabs.hide();
        this.tab.click(this.onTabClicked.bind(this));
        this.nextBtn.click(this.onNextClicked.bind(this));
        this.prevBtn.click(this.onPrevClicked.bind(this));
        //this.submitBtn.click(this.onSubmitClicked.bind(this));
        this.$form.submit(this.onSubmitClicked.bind(this));
        this.paiementChoiceBtn.click(this.inputUpdate.bind(this));
        this.tabCount = this.tab.length;
        this.update();
    };

    Checkout.prototype.inputUpdate = function(event){
        var choice = $(event.target).parents(".choice");
        var input = choice.find('[type="radio"]');
        console.log("Input clicked : Value : ");
        this.paiementChoiceBtn.removeClass("active");
        this.$inputs.removeAttr('checked');
        choice.addClass("active");
        input.attr('checked', 'true');
        this.nextBtn.removeClass("disabled");
        console.log(input);
        console.log(choice);
    };
    Checkout.prototype.onNextClicked = function(event){
        
        
        if(this.currentTab != 1){
            this.tab.removeClass("active");
            this.currentTab = (this.currentTab + 1 ) % this.tabCount;
            this.update();
        }
        else{
            console.log("Checking for checked input");
            if(this.isInputChecked()){
                this.tab.removeClass("active");
                this.currentTab = (this.currentTab + 1 ) % this.tabCount;
                //this.nextBtn.removeClass("disabled");
                this.update();
            }
            else{
                console.log("No valid input found");
                //this.nextBtn.addClass("disabled");
            }
        }
        

    };
    Checkout.prototype.isInputChecked = function(){
        return $('input:checked').length == 1;
    };
    Checkout.prototype.onPrevClicked = function(event){
        this.tab.removeClass("active");
        this.currentTab = (this.currentTab - 1 ) % this.tabCount;
        this.update();
    };
    Checkout.prototype.onSubmitClicked = function(event){
        console.log("Checkout is being submitted")
        //event.stopPropagation();
        //event.preventDefault();
        return true;
    };

    Checkout.prototype.onTabClicked = function(event){
        event.stopPropagation();
        var tab = parseInt($(event.target).data("index"));
        if(tab == 2){
            if(this.isInputChecked()){
                this.currentTab = tab;
                console.log("there is one input checked");
                this.update();
            }
            else
                console.log("there is no input checked");
        }
        else if( (tab != this.currentTab) && (tab < 3) && (tab >= 0)){
            
            this.currentTab = tab;
            this.update();
        }
    };

    Checkout.prototype.update = function(){
        if( (this.currentTab == 1) && !this.isInputChecked()){
            this.nextBtn.addClass("disabled");
        }
        else{
            this.nextBtn.removeClass("disabled");
        }
        this.tab.removeClass("active");
        $(this.tab[this.currentTab]).addClass("active");
        if(this.currentTab > 0){
            this.prevBtn.show();
        }
        else{
            this.prevBtn.hide();
        }
        if(this.currentTab == (this.tabCount - 1)){
            this.nextBtn.hide();
        }
        else{
            this.nextBtn.show();
        }
        this.tabs.hide();
        $(this.tabs[this.currentTab]).show();
        if(this.currentTab == 2){
            this.submitBtn.show();
        }
        else{
            this.submitBtn.hide();
        }
    };
    return Checkout;
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
Shopping.cart  = new Shopping.Cart();
Shopping.account = new Account();
Shopping.catalog = new Catalog();
Shopping.wishlist =  new Wishlist();
Shopping.checkout = new Checkout();
Shopping.catalog.init(0);
Shopping.account.init();
Shopping.cart.init();
Shopping.wishlist.init();
Shopping.checkout.init();
Shopping.wishlist.addCatalog(Shopping.catalog);
Shopping.cart.addCatalog(Shopping.catalog);
Shopping.collapsible = new Collapsible();
Shopping.collapsible.init();
Shopping.modal = new Modal();
Shopping.modal.init();
Shopping.tabs = new Tabs();
Shopping.tabs.init();
