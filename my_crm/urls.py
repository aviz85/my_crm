from django.urls import path
from initial_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('customers/', views.customer_management, name='customer_management'),
    path('orders/', views.order_management, name='order_management'),
    path('customers/edit/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('orders/edit/<int:order_id>/', views.edit_order, name='edit_order'),
]