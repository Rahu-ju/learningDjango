from carts.models import Cart
from .models import Order


class CartOrderMixin:
    # return the cart object by creating or retriving from databse.
    def get_cart(self, *args, **kwargs):
        cart_id = self.request.session.get('cart_id')
        if cart_id == None:
            return None
        cart = Cart.objects.get(id=cart_id)
        if cart.items.count() <= 0:
            return None
        return cart

    # Return the order object by creating or retriving from databse
    def get_order(self, *args, **kwargs):
        # if new_order_id exist in the session then it retrive
        # the order therwise it create a new order instance and feed the id
        # to the session.

        #""" Lession to learn:
        # create is use when you need the id of that instance(because it save the model)
        # instance = Model() is used when you step by step feed the data to the instance."""
        cart = self.get_cart()
        if cart == None:
            return None
        new_order_id = self.request.session.get("new_order_id")
        if new_order_id is None:
            new_order = Order.objects.create(cart=cart)
            self.request.session["new_order_id"] = new_order.id
            return new_order
        new_order = Order.objects.get(id=new_order_id)
        return new_order
