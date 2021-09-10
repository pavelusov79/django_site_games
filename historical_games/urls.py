"""historical_games URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.conf import settings
from django.urls import include, path

from mainapp.views import SearchResultsView, NewsListView, NewsDetailView, ContactsFormView, ProductListView, \
    ProductDetailView, HomeView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', include('adminapp.urls', namespace='admin')),
    path('order/', include('ordersapp.urls', namespace='order')),
    path('', include('social_django.urls', namespace='social')),
    path('', HomeView.as_view(), name='main'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    path('contacts/', ContactsFormView.as_view(), name='contacts'),
    path('thanks/', TemplateView.as_view(template_name='mainapp/thanks.html', extra_context={'title': 'success'}), name='thanks'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('about/', TemplateView.as_view(template_name='mainapp/about.html', extra_context={'title': 'About'}), name='about'),
    path('news/', NewsListView.as_view(), name='news'),
    path('news_<int:pk>/', NewsDetailView.as_view(), name="news_detail"),
    path('team/', TemplateView.as_view(template_name='mainapp/team.html', extra_context={'title': 'Team'}), name='team'),
    path('services/', TemplateView.as_view(template_name='mainapp/services.html', extra_context={'title': 'Services'}), name='services'),
    path('search/', SearchResultsView.as_view(), name="search_results")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
