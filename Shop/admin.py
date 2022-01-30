from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import  OrderItem, ban, cart, category, mainslide, order, product,art 
from .models import con ,MAINPAGEPRODUCTS
# Register your models here.

admin.site.register(category)
admin.site.register(product)

admin.site.register(con)

admin.site.register(MAINPAGEPRODUCTS)

admin.site.register(art)

admin.site.register(mainslide)
admin.site.register(cart)
admin.site.register(ban)
admin.site.register(order)
admin.site.register(OrderItem)