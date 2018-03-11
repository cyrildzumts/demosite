import json
from django.shortcuts import render
from wishlist.models import Wishlist, WishlistItem
from wishlist import wishlist
from django.conf import settings
from django.shortcuts import render
from catalog.models import Product
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required
def show_wishlist(request):
    template_name = "wishlist/wishlist.html"
    user_wishlist = wishlist.get_wishlist(request.user)

    wishlistitems = user_wishlist.get_items()
    page_title = 'Liste des souhaits' + " - " + settings.SITE_NAME
    item_count = user_wishlist.items_count()

    context = {'wishlistitems': wishlistitems,
               'page_title': page_title,
               'item_count': item_count,
              }
    return render(request=request,
                  template_name=template_name,
                  context=context)

def add_to_wishlist(request, item_id):
    template_name = "wishlist/wishlist.html"
    user_wishlist = wishlist.get_wishlist(request.user)

    user_wishlist.add(int(item_id))
    wishlistitems = user_wishlist.wishlistitem_set.all()
    page_title = 'Liste des souhaits' + " - " + settings.SITE_NAME
    item_count = user_wishlist.items_count()
    context = {'wishlistitems': wishlistitems,
               'page_title': page_title,
               'item_count': item_count,
              }
    return render(request=request,
                  template_name=template_name,
                  context=context)

@csrf_exempt
def remove_from_wishlist(request, item_id):
    """
    This method remove an item from the user's
    wishlist.
    """
    template_name = "wishlist/wishlist.html"
    user_wishlist = wishlist.get_wishlist(request.user)
    user_wishlist.remove(int(item_id))
    page_title = 'Liste des souhaits' + " - " + settings.SITE_NAME
    item_count = user_wishlist.items_count()
    wishlistitems = user_wishlist.get_items()
    context = {'wishlistitems': wishlistitems,
               'page_title': page_title,
               'item_count': item_count,
              }
    return render(request=request,
                  template_name=template_name,
                  context=context)
@csrf_exempt
def clear(request):
    """
    This view allows the user to all items from
    the wishlist.
    """
    #print("Clear Wishlist requested")
    template_name = "wishlist/wishlist.html"
    user_wishlist = wishlist.get_wishlist(request.user)
    user_wishlist.clear()
    #wishlistitems = user_wishlist.get_items()
    wishlistitems = None
    page_title = 'Liste des souhaits' + " - " + settings.SITE_NAME
    item_count = user_wishlist.items_count()

    context = {'wishlistitems': wishlistitems,
               'page_title': page_title,
               'item_count': item_count,
              }
    return render(request=request,
                  template_name=template_name,
                  context=context)

@csrf_exempt
def ajax_remove_from_wishlist(request):
    """
    This method process ajax request.
    This method remove an item from the user's
    wishlist. The Request object contains the
    item ID.
    """
    response = {}
    jsonresponse = HttpResponseBadRequest()
    request_is_valid = len(request.POST) > 0
    flag = False
    if request_is_valid:
        postdata = request.POST.copy()
        product_id = int(postdata['product_id'])
        user_wishlist = wishlist.get_wishlist(request.user)
        flag = user_wishlist.remove(int(product_id))
        item_count = user_wishlist.items_count()
        response = {'state': flag,
                    'item_count': item_count,
                   }
        jsonresponse = HttpResponse(json.dumps(response), content_type="application/json")
    return jsonresponse

@csrf_exempt
def ajax_add_to_wishlist(request):
    """
    This method process ajax request.
    This method add an item into the user's
    wishlist. The Request object contains the
    item ID.
    """
    #Fix-me
    # To-Do : When the client is trying to add an item that is already
    # in the wishlist, the view should inform the client about that.
    response = {}
    jsonresponse = HttpResponseBadRequest()
    request_is_valid = len(request.POST) > 0
    if request_is_valid:
        postdata = request.POST.copy()
        product_id = int(postdata['product_id'])
        user_wishlist = wishlist.get_wishlist(request.user)
        res = user_wishlist.add(int(product_id))
        item_count = user_wishlist.items_count()
        response = {'added': res['added'],
                    'duplicated': res['duplicated'],
                    'item_count': item_count,
                   }
        jsonresponse = HttpResponse(json.dumps(response), content_type="application/json")
    return jsonresponse


@csrf_exempt
def ajax_wishlist_clear(request):
    """
    This view allows the user to all items from
    the wishlist.
    """
    user_wishlist = wishlist.get_wishlist(request.user)
    user_wishlist.clear()
    print("User %s Wishlist cleared" % request.user.username)
    item_count = user_wishlist.items_count()
    response = {}
    item_count = user_wishlist.items_count()
    response = {'state': True,
                'item_count': item_count,
            }
    jsonresponse = HttpResponse(json.dumps(response), content_type="application/json")
    return jsonresponse