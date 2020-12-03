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
from mainapp import views
from django.conf import settings
from django.urls import include, path

from mainapp.views import SearchResultsView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', include('adminapp.urls', namespace='admin')),
    path('order/', include('ordersapp.urls', namespace='order')),
    path('', include('social_django.urls', namespace='social')),
    path('', views.main, name="main"),
    # path('catalog/', views.catalog, name="catalog"),
    path('page/<int:page>', views.catalog, name="page"),
    path('contacts/', views.contacts, name="contacts"),
    path('contacts/thanks/', views.thanks, name='thanks'),
    path('catalog/<int:pk>', views.product_page, name="product_page"),
    path('discount/<int:pk>/', views.product_discount, name="discount"),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('about/', views.about, name="about"),
    path('news/<int:page>/', views.news, name="news"),
    path('news/detail/<int:pk>', views.news_detail, name="news_detail"),
    path('team/', views.team, name="team"),
    path('services', views.services, name="services"),
    path('search/', SearchResultsView.as_view(), name="search_results")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
