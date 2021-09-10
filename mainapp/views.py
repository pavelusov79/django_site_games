from itertools import chain

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail

from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.views.generic.edit import FormMixin

from .models import Product, News, Subscribe
from django.db.models import Q
from mainapp.forms import ContactForm, SubscribeForm


class ContactsFormView(FormView):
    template_name = 'mainapp/contacts.html'
    form_class = ContactForm
    success_url = '/thanks/'
    extra_context = {'title': 'Contacts'}

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        recipients = ['usov.p@mail.ru']

        send_mail('сообщение с сайта historical_games',
                       f'от: {name}\nemail: {email}\n{message}', DEFAULT_FROM_EMAIL, recipients)

        return super().form_valid(form)


class HomeView(FormMixin, TemplateView):
    template_name = 'mainapp/index.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['products'] = Product.objects.filter(category__is_active=True).order_by('?')[:4]
        context['news_item'] = News.objects.filter(is_active=True).order_by('-published')[:3]
        context['subscribe_form'] = SubscribeForm()
        return context

    def post(self, request, *args, **kwargs):
        form = SubscribeForm(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        view = ContactsFormView.as_view()
        return view(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            client_email = form.cleaned_data['client_email']
            subscribe = Subscribe.objects.filter(client_email=client_email, checked=False).first()
            if not subscribe:
                Subscribe.objects.create(client_email=client_email, checked=False, is_active=True)
        return super().form_valid(form)


class ProductListView(FormMixin, ListView):
    model = Product
    queryset = Product.objects.filter(category__is_active=True, is_active=True).order_by('?')
    paginate_by = 8
    context_object_name = 'products'
    form_class = ContactForm
    success_url = '/thanks/'

    def post(self, request, *args, **kwargs):
        view = ContactsFormView.as_view()
        return view(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disc_products'] = Product.objects.filter(Q(category__is_active=True) & Q(quantity__gte=200)).order_by('?')[:2]
        context['title'] = 'Catalog'
        return context


class ProductDetailView(FormMixin, DetailView):
    model = Product
    form_class = ContactForm
    success_url = '/thanks/'

    def post(self, request, *args, **kwargs):
        view = ContactsFormView.as_view()
        return view(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['similar_products'] = Product.objects.filter(category__is_active=True, category=self.object.category).exclude(name=self.object.name).order_by('?')[:4].select_related('category')
        context['title'] = self.object.name
        context['discount_products'] = Product.objects.filter(category__is_active=True, quantity__gte=200).exclude(name=self.object.name).order_by('?')[:4]
        return context


class NewsListView(ListView):
    model = News
    queryset = News.objects.filter(is_active=True).order_by('-published')
    paginate_by = 3
    context_object_name = 'news'
    extra_context = {'title': 'News'}


class NewsDetailView(DetailView):
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.pk
        return context


class SearchResultsView(ListView):
    template_name = 'mainapp/search_list.html'
    extra_context = {'title': 'Поиск'}

    def get_queryset(self):
        query = self.request.GET.get('q')
        query_sets = []
        query_sets.append(News.objects.filter(Q(title__icontains=query)|Q(
            short_desc__icontains=query)).filter(is_active=True).order_by('-published'))
        query_sets.append(Product.objects.filter(name__icontains=query).filter(is_active=True))
        object_list = list(chain(*query_sets))
        return object_list
