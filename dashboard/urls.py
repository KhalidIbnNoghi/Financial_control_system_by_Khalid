from django.urls import path
from dashboard.views import HomePageView, CategoryAddView


urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("category_add/", CategoryAddView.as_view(), name='category_add'),
]
