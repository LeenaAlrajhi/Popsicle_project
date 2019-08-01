from django import template
from django.contrib.auth.models import User
from final_app.models import Order

register = template.Library()

@register.filter
def cart_products_count(user) :
    if user.is_authenticated :
        orderـcurrent = Order.objects.filter(user = user, ordered = False)

        if orderـcurrent.exists() :
            return orderـcurrent[0].products.count()

    return 0