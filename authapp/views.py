from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserProfileEditForm
from django.contrib import auth
from django.urls import reverse

from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение почты {user.email}'
    message = settings.DOMAIN_NAME + verify_link

    return send_mail(title, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        setattr(user, 'backend', 'django.contrib.auth.backends.ModelBackend')
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'error user activation {email}')
            return render(request, 'authapp/verification.html')
    except Exception as ex:
        print(f'exception {ex.args}')
        return HttpResponseRedirect(reverse('main'))


def login(request):
    title = 'вход'
    
    login_form = ShopUserLoginForm(data=request.POST or None)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))

    content = {'title': title, 'login_form': login_form, 'next': next}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))
    

def email_verify(request):
    title = 'подтверждение почты'
    context = {'title': title}
    return render(request, 'authapp/email_verify.html', context)


def register(request):
    title = 'регистрация'
    
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
    
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('email sending success')
                # return HttpResponseRedirect(reverse('auth:login'))
                return HttpResponseRedirect(reverse('auth:email_verify'))
            else:
                print('error while email sending')
                # return HttpResponseRedirect(reverse('auth:login'))
                return HttpResponse('ошибка отправки сообщения о регистрации')
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)
    
    
def edit(request):
    title = 'редактирование'
    
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('main'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)
    
    content = {'title': title, 'edit_form': edit_form, 'profile_form': profile_form}
    
    return render(request, 'authapp/edit.html', content)
