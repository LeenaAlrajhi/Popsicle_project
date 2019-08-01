from django.contrib import admin
from .models import Popsicle, Profile, Order, OrderProduct,Address

admin.site.register(Popsicle)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Address)