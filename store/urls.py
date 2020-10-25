
from django.conf.urls import url

from django.urls import path, include
from . import views


urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="index"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('categories/', views.CategoryList.as_view(), name='category_list'),
	path('categories/<pk>', views.CategoryDetail.as_view(), name='category_detail'),

	path('update_item/', views.updateItem, name='update-item'),
	path('process_order/', views.processOrder, name='process_order'),

]
