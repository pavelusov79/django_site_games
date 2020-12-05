from itertools import chain

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Product, ProdPage, News
from django.shortcuts import get_object_or_404
from django.db.models import Q
from mainapp.forms import ContactForm, SubscribeForm


# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     else:
#         return []


def main(request):
    # gallery_box = [
    # 	{'img': 'img/assasins.png', 'alt': 'assasings', 'name': "Assasin's Creed: Rogue"},
    # 	{'img': 'img/raider.png', 'alt': 'raider', 'name': 'Tomb Raider'},
    # 	{'img': 'img/ryse.png', 'alt': 'ryse', 'name': 'Ryse: Son of Rome'},
    # 	{'img': 'img/warcraft.png', 'alt': 'warcraft', 'name': 'World of Warcraft: Wrath of The Linch King'}
    # ]
    products = Product.objects.filter(category__is_active=True).exclude(quantity__gte=200).order_by('?')[:4]
    news_item = News.objects.filter(is_active=True).order_by('-published')[:3]
    # basket = get_basket(request.user)
    sent = False
    subscribe_form = SubscribeForm()
    form = ContactForm()
    if request.method == 'POST' and subscribe_form:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            client_email = subscribe_form.cleaned_data['client_email']
            sent = True
            subscribe_form.save()
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
        # 'gallery_box': gallery_box
        'products': products,
        # 'basket': basket
        'news_item': news_item,
        'form': form,
        'sent': sent,
        'subscribe_form': subscribe_form
    }
    return render(request, 'mainapp/index.html', context)


def catalog(request, page=1):
    # gallery_box = [
    # 	{'img': 'img/cat-movie_1.png', 'alt': 'game', 'name': 'BUTTLEFIELD 1'},
    # 	{'img': 'img/cat-movie_2.png', 'alt': 'game', 'name': 'STAR WARS: Buttlefront II'},
    # 	{'img': 'img/cat-movie_3.png', 'alt': 'game', 'name': 'BUTTELFIELD 4'},
    # 	{'img': 'img/cat-movie_4.png', 'alt': 'game', 'name': 'WORLD OF TANKS'}
    # ]
    # gallery_box2 = [
    # 	{'img': 'img/assasins.png', 'alt': 'game', 'name': "ASSASIN'S CREED: Rogue"},
    # 	{'img': 'img/cat-movie_5.png', 'alt': 'game', 'name': 'FOR HONOR'},
    # 	{'img': 'img/cat-movie_6.png', 'alt': 'game', 'name': 'WORLD OF WARSHIPS'},
    # 	{'img': 'img/cat-movie_7.png', 'alt': 'game', 'name': 'CALL OF DUTY Infinite Warface'}
    # ]

    # disc_products = Product.objects.filter(category__is_active=True).filter(quantity__gte=200).order_by('?')[:2]
    disc_products = Product.objects.filter(Q(category__is_active=True) & Q(quantity__gte=200)).order_by('?')[:2]
    products = Product.objects.filter(category__is_active=True, is_active=True).order_by('?').exclude(quantity__gte=200)
    # basket = get_basket(request.user)
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
        # 'gallery_box': gallery_box,
        # 'gallery_box2': gallery_box2
        'products': prod_paginator,
        'disc_products': disc_products,
        # 'basket': basket
        'form': form
    }
    return render(request, 'mainapp/catalog.html', context)


def contacts(request):
    # basket = get_basket(request.user)
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
        # 'basket': basket
        'form': form
    }
    return render(request, 'mainapp/contacts.html', context)


def product_page(request, pk):
    prod_img = get_object_or_404(ProdPage, pk=pk)
    title_prod = get_object_or_404(Product, pk=pk)
    similar_products = Product.objects.filter(category__is_active=True).exclude(name=title_prod.name).exclude(quantity__gte=200).filter(
        category=title_prod.category).order_by('?')[:4]
    title = title_prod.name
    # basket = get_basket(request.user)

    # with open("json.json") as f:
    # 	data = json.load(f)
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
        # 'data': data
        'prod_img': prod_img,
        'title_prod': title_prod,
        'similar_products': similar_products,
        'form': form
        # 'basket': basket
    }
    return render(request, 'mainapp/product_page.html', context)


def product_discount(request, pk):
    disc_img = get_object_or_404(ProdPage, pk=pk)
    title_prod = get_object_or_404(Product, pk=pk)
    discount_products = Product.objects.filter(category__is_active=True).exclude(name=title_prod.name).filter(
        quantity__gte=200).order_by('?')[:4]
    title = title_prod.name
    # basket = get_basket(request.user)
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
        # 'basket': basket
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
    # page = request.GET.get('page')
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
