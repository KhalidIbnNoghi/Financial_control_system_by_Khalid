from django.urls import path
from django.contrib.auth import views as auth_views
from dashboard.views import HomePageView, CategoryAddView, PaymentAddView, PaymentHistoryView
from . import views

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("category_add/", CategoryAddView.as_view(), name='category_add'),
    path("payment_add/<int:pk>", PaymentAddView.as_view(), name='payment_add'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('payment_history', PaymentHistoryView.as_view(), name='payment-history'),
    path('password-change/',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
]
