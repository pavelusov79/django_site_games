from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.generic import ListView, DeleteView

from basketapp.models import Basket
from mainapp.models import Product 
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import F


class BasketView(ListView):
    model = Basket
    extra_context = {'title': "Basket"}
    template_name = 'basketapp/basket.html'

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user).order_by('product__price')


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('catalog', args=[pk]))
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()
    if not basket:
        basket = Basket(user=request.user, product=product)
    basket.quantity += 1
    if basket.quantity:
        Basket.objects.filter(user=request.user, product=product).update(quantity=F('quantity') + 1)
    basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        new_basket_item = Basket.objects.get(pk=int(pk))
        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()
        basket_items = Basket.objects.filter(user=request.user).order_by('product__price')
        content = {'basket_items': basket_items}
        result = render_to_string('basketapp/includes/inc_basket_list.html', content)
        return JsonResponse({'result': result})


