from django.urls import path
from django.contrib.auth import views as auth_views
from dashboard.views import HomePageView, CategoryAddView, PaymentAddView
from . import views

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("category_add/", CategoryAddView.as_view(), name='category_add'),
    path("payment_add/<int:pk>", PaymentAddView.as_view(), name='payment_add'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
]
