from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/update_item/<int:pk>/', views.UpdateCartItemView.as_view(), name='update_cart_item'),
    path('cart/add_item/<int:pk>/', views.AddCartItemView.as_view(), name='add_cart_item'),
    path('cart/delete_item/<int:pk>/', views.DeleteCartItemView.as_view(), name='delete_cart_item'),
    
]