from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, \
    ProductCategoryEditForm, ProductEditForm, NewsEditForm, SubscribeForm

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory, ProdPage, News, Subscribe
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db.models import F


# @user_passes_test(lambda u: u.is_superuser)
# def users(request: object):
#     title = 'Админка / Пользователи'
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     content = {'title': title, 'objects': users_list}
#
#     return render(request, 'adminapp/users.html', content)


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка / Пользователи'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'Пользователи / Создание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     content = {'title': title, 'update_form': user_form}
#
#     return render(request, 'adminapp/user_update.html', content)

class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = '__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи / Создание'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'Пользователи / Редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
#
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     content = {'title': title, 'update_form': edit_form}
#
#     return render(request, 'adminapp/user_update.html', content)

class UserEditView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи / Редактирование'

        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'Пользователи / Удаление'
#
#     user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         if user.is_active:
#             user.is_active = False
#         else:
#             user.is_active = True
#         user.save()
#         return HttpResponseRedirect(reverse('admin:users'))
#
#     content = {'title': title, 'user_to_delete': user}
#
#     return render(request, 'adminapp/user_delete.html', content)


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи / Удаление'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(reverse('admin:users'))


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'Категории / Создание'
#
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         category_form = ProductCategoryEditForm()
#
#     content = {'title': title, 'update_form': category_form}
#
#     return render(request, 'adminapp/category_update.html', content)


class NewsCreateView(CreateView):
    model = News
    template_name = 'adminapp/news_update.html'
    success_url = reverse_lazy('admin:news_page', args=[1])
    form_class = NewsEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости / Создание'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def news(request):
#     title = 'Админка / Новости'
#     news_content = News.objects.all().order_by('-published')
#     # paginator = Paginator(news_content, 3)
#     # try:
#     #     news_paginator = paginator.page(page)
#     # except PageNotAnInteger:
#     #     news_paginator = paginator.page(1)
#     # except EmptyPage:
#     #     news_paginator = paginator.page(paginator.num_pages)
#
#     content = {'title': title, 'objects': news_content}
#
#     return render(request, 'adminapp/news.html', content)


class NewsListView(ListView):
    paginate_by = 3
    model = News
    template_name = 'adminapp/news.html'
    ordering = ['-published']

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # def get_queryset(self):
    #     return News.objects.all().order_by('-published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка / Новости'

        return context


class NewsEditView(UpdateView):
    model = News
    template_name = 'adminapp/news_update.html'
    success_url = reverse_lazy('admin:news_page', args=[1])
    form_class = NewsEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости / Редактирование'
        return context


class NewsDetailView(DetailView):
    model = News
    template_name = 'adminapp/news_detail.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости / Отдельная новость'
        return context


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'adminapp/news_delete.html'
    success_url = reverse_lazy('admin:news_page', args=[1])

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости / Удаление'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(reverse('admin:news_page'))


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории / Создание'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'Админка / Категории'
#     categories_list = ProductCategory.objects.all()
#
#     content = {'title': title, 'objects': categories_list}
#
#     return render(request, 'adminapp/categories.html', content)

class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка / Категории'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'Категории / Редактирование'
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, instance=edit_category)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         category_form = ProductCategoryEditForm(instance=edit_category)
#
#     content = {'title': title, 'update_form': category_form}
#
#     return render(request, 'adminapp/category_update.html', content)

class CategoryEditView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории / Редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))

        return super().form_valid(form)


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        # db_profile_by_type(sender, 'UPDATE', connection.queries)


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'Категории / Удаление'
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         if category_item.is_active:
#             category_item.is_active = False
#         else:
#             category_item.is_active = True
#         category_item.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#
#     content = {'title': title, 'category_to_delete': category_item}
#
#     return render(request, 'adminapp/category_delete.html', content)


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории / Удаление'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(reverse(self.success_url))


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'Продукты / Создание'
    prod_cat = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[prod_cat.pk]))
    else:
        product_form = ProductEditForm()

    content = {'title': title, 'category': prod_cat, 'update_form': product_form}

    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk, page=1):
    title = 'Админка / Продукт'
    category = get_object_or_404(ProductCategory, pk=pk)
    product_list = Product.objects.filter(category__pk=pk, category__is_active=True).order_by(
        'price')
    paginator = Paginator(product_list, 2)
    try:
        prod_paginator = paginator.page(page)
    except PageNotAnInteger:
        prod_paginator = paginator.page(1)
    except EmptyPage:
        prod_paginator = paginator.page(paginator.num_pages)

    content = {'title': title, 'category': category, 'objects': prod_paginator}

    return render(request, 'adminapp/products.html', content)


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'Продукты / Карточка товара'
#     prod_image = get_object_or_404(ProdPage, pk=pk)
#     content = {'title': title, 'prod': prod_image}
#
#     return render(request, 'adminapp/product.html', content)

class ProductDetailView(DetailView):
    model = ProdPage
    template_name = 'adminapp/product.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продукты / Карточка товара'
        return context


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'Продукты / Редактирование'
    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[edit_product.category.pk]))
    else:
        product_form = ProductEditForm(instance=edit_product)

    content = {'title': title, 'category': edit_product.category, 'update_form': product_form}

    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'Продукты / Удаление'
    product_item = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        if product_item.is_active:
            product_item.is_active = False
        else:
            product_item.is_active = True
        product_item.save()
        return HttpResponseRedirect(reverse('admin:products', args=[product_item.category.pk]))

    content = {'title': title, 'product_to_delete': product_item}

    return render(request, 'adminapp/product_delete.html', content)


# class SubscribersListView(ListView):
#     model = Subscribe
#     template_name = 'adminapp/subscribers.html'
#
#     @method_decorator(user_passes_test(lambda u: u.is_superuser))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Админка / Подписчики'
#         return context


@user_passes_test(lambda u: u.is_superuser)
def subscribers(request):
    title = 'Админка / Подписчики'
    subscribers_list = Subscribe.objects.all()
    check = SubscribeForm()

    content = {'title': title, 'objects': subscribers_list, 'field': check}

    return render(request, 'adminapp/subscribers.html', content)


@user_passes_test(lambda u: u.is_superuser)
def subscribers_delete(request):
    title = 'Админка / Удаление подписчиков'
    sub_list = Subscribe.objects.all()
    form = SubscribeForm()
    field = sub_list.first()
    if request.method == "POST":
        for field in sub_list:
            if field.is_active:
                field.is_active = False
            else:
                field.is_active = True
        return HttpResponseRedirect(reverse_lazy('admin:subscribers'))
    content = {'title': title,
               'object': field,
               'form': form
               }

    return render(request, 'adminapp/sub_delete.html', content)
