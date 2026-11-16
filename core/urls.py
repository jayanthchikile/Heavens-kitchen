from django.urls import path
from . import views   # ✅ correct place

urlpatterns = [
    path('', views.home, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),  # ✅ FIXED
    path('booking/', views.booking_view, name='booking'),
    path('delete-booking/<int:id>/', views.delete_booking, name='delete_booking'),
    path('edit-booking/<int:id>/', views.edit_booking, name='edit_booking'),
    path('payment/', views.payment_view, name='payment'),
    path('menu/', views.menu_view, name='menu'),
    path('delete-order/<int:id>/', views.delete_order, name='delete_order'),
    path('edit-order/<int:id>/', views.edit_order, name='edit_order'),
    path('orders/', views.orders_view, name='orders'),
]