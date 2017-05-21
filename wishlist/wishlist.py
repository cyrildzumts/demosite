from wishlist.models import Wishlist

def get_wishlist(user):
    """
        @brief get_wishlist
        @param user :  the current user who made the request
        @ return a Cart which belongs to user.
        if the user has no Wishlist, then a new one is created for this user
    """
    try:
        wishlist = Wishlist.objects.get(user=user)
    except Wishlist.DoesNotExist:
        wishlist = Wishlist()
        wishlist.user = user
        wishlist.save()
    return wishlist