from django.shortcuts import render
from wishlist.models import Wishlist, WishlistItem
from wishlist import wishlist
from django.conf import settings

# Create your views here.
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


def remove_from_wishlist(request, item_id):
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