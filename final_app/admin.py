from django.contrib import admin
from .models import Popsicle, Profile, Order, OrderProduct

admin.site.register(Popsicle)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderProduct)