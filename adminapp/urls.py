from django.urls import path

import adminapp.views as adminapp

app_name = "adminapp"

urlpatterns = [
	path('users/create/', adminapp.UserCreateView.as_view(), name='user_create'),
	path('users/read/', adminapp.UsersListView.as_view(), name='users'),
	path('users/update/<int:pk>/', adminapp.UserEditView.as_view(), name='user_update'),
	path('users/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),
	path('categories/create/', adminapp.CategoryCreateView.as_view(), name='category_create'),
	path('categories/read/', adminapp.CategoriesListView.as_view(), name='categories'),
	path('categories/update/<int:pk>/', adminapp.CategoryEditView.as_view(), name='category_update'),
	path('categories/delete/<int:pk>/', adminapp.CategoryDeleteView.as_view(), name='category_delete'),
	path('news/create/', adminapp.NewsCreateView.as_view(), name='news_create'),
	path('news/<int:page>/', adminapp.NewsListView.as_view(), name='news_page'),
	path('news/read/<int:pk>/', adminapp.NewsDetailView.as_view(), name='news_read'),
	path('news/update/<int:pk>/', adminapp.NewsEditView.as_view(), name='news_update'),
	path('news/delete/<int:pk>/', adminapp.NewsDeleteView.as_view(), name='news_delete'),
	path('subscribers/', adminapp.SubscribersListView.as_view(), name='subscribers'),
	path('product/create/category/<int:pk>/', adminapp.ProductCreateView.as_view(), name='product_create'),
	path('product/read/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_read'),
	path('products/read/category/<int:pk>/', adminapp.ProductsListView.as_view(), name='products'),
	path('product/update/<int:pk>/', adminapp.ProductUpdateView.as_view(), name='product_update'),
	path('product/delete/<int:pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete')

]
