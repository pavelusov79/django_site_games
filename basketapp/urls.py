from django.contrib.auth.decorators import login_required
from django.urls import path

import basketapp.views as basketapp

app_name = "basketapp"

urlpatterns = [
	path('', login_required(basketapp.BasketView.as_view()), name='view'),
	path('add/<int:pk>', basketapp.basket_add, name="add"),
	path('remove/<int:pk>', basketapp.basket_remove, name="remove"),
	path('edit/<int:pk>/<int:quantity>/', basketapp.basket_edit, name="edit"),
]
