from django.urls import path
from . import views

urlpatterns = [
	path('', views.ApiOverview, name='home'),
	path('create/',views.add_product, name='add_product'),
	path('all/', views.view_products, name='view_products'),
	path('update/<str:pk>/', views.update_products, name='update_products'),
	path('delete/<str:pk>/', views.delete_products, name='delete_products'),
	path('register/',views.RegisterUserAPIView.as_view()),
	path('login/', views.login_view, name="login_view"),
	# path('addcart/',views.CartView.as_view()),

]