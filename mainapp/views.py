from itertools import chain

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Product, ProdPage, News, Subscribe
from django.shortcuts import get_object_or_404
from django.db.models import Q
from mainapp.forms import ContactForm, SubscribeForm


def main(request):
    products = Product.objects.filter(category__is_active=True).exclude(quantity__gte=200).order_by('?')[:4]
    news_item = News.objects.filter(is_active=True).order_by('-published')[:3]
    subscribe_form = SubscribeForm()
    form = ContactForm()
    if request.method == 'POST' and subscribe_form:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            client_email = subscribe_form.cleaned_data['client_email']
            subscribe = Subscribe.objects.filter(client_email=client_email, checked=False).first()
            if not subscribe:
                Subscribe.objects.create(client_email=client_email, checked=False, is_active=True)
        else:
            subscribe_form = SubscribeForm()

    elif request.method == 'POST' and form:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            recipients = ['usov.p@mail.ru']

            send_mail('сообщение с сайта historical_games',
                      f'от: {name}\nemail: {email}\n{message}', DEFAULT_FROM_EMAIL, recipients)
            return render(request, 'mainapp/thanks.html')

        else:
            form = ContactForm()

    context = {
        'title': "Home",
        'products': products,
        'news_item': news_item,
        'form': form,
        'subscribe_form': subscribe_form
    }
    return render(request, 'mainapp/index.html', context)


def catalog(request, page=1):
    disc_products = Product.objects.filter(Q(category__is_active=True) & Q(quantity__gte=200)).order_by('?')[:2]
    products = Product.objects.filter(category__is_active=True, is_active=True).order_by('?').exclude(quantity__gte=200)
    paginator = Paginator(products, 8)
    try:
        prod_paginator = paginator.page(page)
    except PageNotAnInteger:
        prod_paginator = paginator.page(1)
    except EmptyPage:
        prod_paginator = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            recipients = ('usov.p@mail.ru', )

            send_mail('сообщение с сайта historical_games',
                      f'от: {name}\nemail: {email}\n{message}', DEFAULT_FROM_EMAIL, recipients)
            return render(request, 'mainapp/thanks.html')

    else:
        form = ContactForm()
    context = {
        'title': "Catalog",
        'products': prod_paginator,
        'disc_products': disc_products,
        'form': form
    }
    return render(request, 'mainapp/catalog.html', context)


def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            recipients = ['usov.p@mail.ru']

            send_mail('сообщение с сайта historical_games',
                      f'от: {name}\nemail: {email}\n{message}', DEFAULT_FROM_EMAIL, recipients)
            return render(request, 'mainapp/thanks.html')
    else:
        form = ContactForm()

    context = {
        'title': "Contacts",
        'form': form
    }
    return render(request, 'mainapp/contacts.html', context)


def product_page(request, pk):
    prod_img = get_object_or_404(ProdPage, pk=pk)
    title_prod = get_object_or_404(Product, pk=pk)
    similar_products = Product.objects.filter(category__is_active=True).exclude(name=title_prod.name).exclude(quantity__gte=200).filter(
        category=title_prod.category).order_by('?')[:4]
    title = title_prod.name

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            recipients = ['usov.p@mail.ru']

            send_mail('сообщение с сайта historical_games',
                      f'от: {name}\nemail: {email}\n{message}', DEFAULT_FROM_EMAIL, recipients)
            return render(request, 'mainapp/thanks.html')
    else:
        form = ContactForm()

    context = {
        'title': title,
        'prod_img': prod_img,
        'title_prod': title_prod,
        'similar_products': similar_products,
        'form': form
    }
    return render(request, 'mainapp/product_page.html', context)


def product_discount(request, pk):
    disc_img = get_object_or_404(ProdPage, pk=pk)
    title_prod = get_object_or_404(Product, pk=pk)
    discount_products = Product.objects.filter(category__is_active=True).exclude(name=title_prod.name).filter(
        quantity__gte=200).order_by('?')[:4]
    title = title_prod.name

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            recipients = ['usov.p@mail.ru']

            send_mail('сообщение с сайта historical_games',
                      f'от: {name}\nemail: {email}\n{message}', DEFAULT_FROM_EMAIL, recipients)
            return render(request, 'mainapp/thanks.html')
    else:
        form = ContactForm()

    context = {
        'title': title,
        'disc_img': disc_img,
        'title_prod': title_prod,
        'discount_products': discount_products,
        'form': form
    }
    return render(request, 'mainapp/product_discount_page.html', context)


def about(request):
    context = {
        'title': "About"
    }
    return render(request, 'mainapp/about.html', context)


def team(request):
    context = {
        'title': "Team"
    }
    return render(request, 'mainapp/team.html', context)


def news(request, page=1):
    news_item = News.objects.filter(is_active=True).order_by('-published')
    paginator = Paginator(news_item, 3)

    try:
        news_paginator = paginator.page(page)
    except PageNotAnInteger:
        news_paginator = paginator.page(1)
    except EmptyPage:
        news_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': "News",
        'news': news_paginator
    }
    return render(request, 'mainapp/news.html', context)


def news_detail(request, pk):
    one_news = News.objects.get(pk=pk)
    title = one_news.pk
    context = {
        'title': title,
        'one_news': one_news
    }
    return render(request, 'mainapp/news_detail.html', context)


def services(request):
    context = {
        'title': "Services"
    }
    return render(request, 'mainapp/services.html', context)


def thanks(request):
    context = {
        'title': "Sent_email_success"
    }
    return render(request, 'mainapp/thanks.html', context)


class SearchResultsView(ListView):
    template_name = 'mainapp/search_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        query_sets = []
        query_sets.append(News.objects.filter(Q(title__icontains=query)|Q(
            short_desc__icontains=query)).filter(is_active=True).order_by('-published'))
        query_sets.append(Product.objects.filter(name__icontains=query).filter(is_active=True))
        object_list = list(chain(*query_sets))
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск'
        return context
