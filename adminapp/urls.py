from django.urls import path

import adminapp.views as adminapp

app_name = "adminapp"

urlpatterns = [
	# path('users/create/', adminapp.user_create, name='user_create'),
	path('users/create/', adminapp.UserCreateView.as_view(), name='user_create'),
	# path('users/read/', adminapp.users, name='users'),
	path('users/read/', adminapp.UsersListView.as_view(), name='users'),
	# path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
	path('users/update/<int:pk>/', adminapp.UserEditView.as_view(), name='user_update'),
	# path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
	path('users/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),

	# path('categories/create/', adminapp.category_create, name='category_create')
	path('categories/create/', adminapp.CategoryCreateView.as_view(), name='category_create'),
	# path('categories/read/', adminapp.categories, name='categories'),
	path('categories/read/', adminapp.CategoriesListView.as_view(), name='categories'),
	# path('categories/update/<int:pk>/', adminapp.category_update, name='category_update'),
	path('categories/update/<int:pk>/', adminapp.CategoryEditView.as_view(), name='category_update'),
	# path('categories/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),
	path('categories/delete/<int:pk>/', adminapp.CategoryDeleteView.as_view(), name='category_delete'),

	path('news/create/', adminapp.NewsCreateView.as_view(), name='news_create'),
	path('news/<int:page>/', adminapp.NewsListView.as_view(), name='news_page'),
	path('news/read/<int:pk>/', adminapp.NewsDetailView.as_view(), name='news_read'),
	path('news/update/<int:pk>/', adminapp.NewsEditView.as_view(), name='news_update'),
	path('news/delete/<int:pk>/', adminapp.NewsDeleteView.as_view(), name='news_delete'),

	# path('subscribers/', adminapp.SubscribersListView.as_view(), name='subscribers'),
	path('subscribers/', adminapp.subscribers, name="subscribers"),
	path('products/create/category/<int:pk>/', adminapp.product_create, name='product_create'),
	path('products/read/category/<int:pk>/', adminapp.products, name='products'),
	path('products/read/category/<int:pk>/<int:page>', adminapp.products, name='page'),
	# path('products/read/<int:pk>/', adminapp.product_read, name='product_read'),
	path('products/read/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_read'),
	path('products/update/<int:pk>/', adminapp.product_update, name='product_update'),
	path('products/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),

]
