
from accounts.models import UserProfile, User
from order.models import Order, OrderItem
from django.core.exceptions import ObjectDoesNotExist


class UserInfoService:

    @staticmethod
    def get_user_name(user_id):
        user_info = None
        if user_id and user_id > 0:
            try:
                user = User.objects.get(id=user_id)
                user_info = {
                    'first_name': user.first_name,
                    'last_name' : user.last_name
                }
            except ObjectDoesNotExist:
                print("query error : no user found with the id : {}".format(user_id))
        
        return user_info
    

    @staticmethod
    def get_user_city(user_id):
        user_info = None
        if user_id and user_id > 0:
            try:
                profile = UserProfile.objects.get(user__id=user_id)
                user_info = {
                    'city': profile.city
                    
                }
            except ObjectDoesNotExist:
                print("query error : no user found with the id : {}".format(user_id))
        
        return user_info
    
    @staticmethod
    def get_user_address(user_id):
        user_info = None
        if user_id and user_id > 0:
            try:
                profile = UserProfile.objects.get(user__id=user_id)
                user_info = {
                    'city': profile.city,
                    'country' : profile.country,
                    'address' : profile.address
                }
            except ObjectDoesNotExist:
                print("query error : no user found with the id : {}".format(user_id))
        
        return user_info
    

    @staticmethod
    def user_is_registered_to_newsletter(user_id):
        done = False
        if user_id and user_id > 0:
            try:
                done = UserProfile.objects.get(user__id=user_id).newsletter
            except ObjectDoesNotExist:
                print("query error : no user found with the id : {}".format(user_id))
        
        return done
    
    

    

    @staticmethod
    def deactivate_user(requester_id, user_id):
        # check first if the requester has the permission to deactivate 
        # an user 
        done = False
        requester = User.objects.get(id=requester_id)
        if(requester.has_perm('accounts:can_change_user:userprofile')):
            r = User.objects.filter(id=user_id).update(is_active=False)
            done = r > 0
            print("CustomerService.deactivate_user() Success : requester user  {} deaticated the user with id {}".format(requester_id, user_id))
        else :
            print("CustomerService.deactivate_user() Error : requester user  {} tried to deaticate the user with id {}".format(requester_id, user_id))
        return done

    
    @staticmethod
    def get_shipping_address(user_id):
        pass


    @staticmethod
    def get_user_phone(user_id):
        user_info = None
        if user_id and user_id > 0:
            try:
                profile = UserProfile.objects.get(user__id=user_id)
                user_info = {
                    'phone': profile.telefon
                }
            except ObjectDoesNotExist:
                print("query error : no user found with the id : {}".format(user_id))
        
        return user_info

    @staticmethod
    def get_last_login(user_id):
        user_info = None
        if user_id and user_id > 0:
            try:
                profile = User.objects.get(id=user_id)
                user_info = {
                    'last_login': profile.last_login

                }
            except ObjectDoesNotExist:
                print("query error : no user found with the id : {}".format(user_id))
        
        return user_info
    

    @staticmethod
    def get_date_joined(user_id):
        user_info = None
        if user_id and user_id > 0:
            try:
                profile = User.objects.get(id=user_id)
                user_info = {
                    'date_joined': profile.date_joined

                }
            except ObjectDoesNotExist:
                print("query error : no user found with the id : {}".format(user_id))
        
        return user_info
    

    @staticmethod
    def get_user_info(user_id):
        user_info = None
        if user_id and user_id > 0:
            try:
                user = User.objects.select_related('userprofile').get(id=user_id)
                user_info = {
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'city': user.userprofile.city,
                    'country': user.userprofile.country,
                    'telefon': user.userprofile.telefon,
                    'date_of_birth': user.userprofile.date_of_birth,
                    'province': user.userprofile.province,
                    'zip_code': user.userprofile.zip_code,
                    'address': user.userprofile.address,
                    'newsletter': user.userprofile.newsletter,
                    'is_staff': user.is_staff,
                    'is_active': user.is_active,
                    'last_login': user.last_login

                }
            except ObjectDoesNotExist:
                print("query error : no user found with the id : {}".format(user_id))
        
        return user_info
    


    @staticmethod
    def get_buyeditems_from_user(user_id):
        queryset = OrderItem.objects.none()
        if user_id and user_id > 0:
            query = ('SELECT order_orderitem.*   from product , auth_user as user '
                'LEFT JOIN order_order  on  order_order.user_id=user.id '
                'LEFT JOIN order_orderitem on order_orderitem.order_id=order_order.id '
                'WHERE Product.id = order_orderitem.product_id and user.id = %s')
            queryset = OrderItem.objects.raw(query, [user_id])
        return queryset
    
    @staticmethod
    def get_user_buyed_items(user_id):
        queryset = OrderItem.objects.none()
        if user_id and user_id > 0:
            try:
                order = Order.objects.filter(user__id=user_id)

            except Order.DoesNotExist 
                pass
