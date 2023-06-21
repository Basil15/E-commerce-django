from django.urls import path
from e_app import views
urlpatterns = [
    path('',views.home,name='home'),
    path('purchase',views.purchase,name='purchase'),
    path('checkout/',views.checkout,name='checkout'),
    path('handlerequest/',views.handlerequest,name='handlerequest'),
    
]
