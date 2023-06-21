from django.contrib import admin
from e_app.models import product,orders,OrderUpdate
# Register your models here.
admin.site.register(product)
admin.site.register(orders)
admin.site.register(OrderUpdate)