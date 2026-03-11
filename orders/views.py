from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from django.views.generic import ListView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Cart,CartItem
from shop.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class CartView(LoginRequiredMixin, ListView):
    template_name = 'cart/cart.html'
    context_object_name = 'cart_items'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        total_amount= sum(item.product.price * item.quantity for item in cart_items)
        context['total_amount'] = total_amount
        return context
    
class AddCartItemView(LoginRequiredMixin, View):
    def get(self, request, pk):
        add_to_cart = True
        product = get_object_or_404(Product, pk=pk)

        try:
            cart, _ = Cart.objects.get_or_create(user=request.user)

            if product.stock > 0:
                cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product=product)
                if not cart_item_created:
                    cart_item.quantity += 1
                elif cart_item_created:
                    cart_item.quantity = 1
                cart_item.save()
            else:
                add_to_cart=False
        except Exception as e:
            return redirect(request.META.get('HTTP_REFERER'))   
        else:
            if add_to_cart:
                messages.success(request, f'Added {product.name} to cart.')
            else:
                messages.error(request, f'Sorry, {product.name} is out of stock.')

            return redirect(request.META.get('HTTP_REFERER'))
        


class DeleteCartItemView(LoginRequiredMixin, DeleteView):
    model = CartItem
    success_url = reverse_lazy('orders:cart')

class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cart_item = CartItem.objects.get(pk=pk, cart__user=request.user)
        new_quantity = int(request.POST.get('quantity', cart_item.quantity))

        if 0 <new_quantity <= cart_item.product.stock:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully.')
        return redirect('orders:cart')

