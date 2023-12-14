from typing import Any
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from dashboard.models import Category

class HomePageView(ListView):
    template_name = 'index.html'
    context_object_name = 'categories'

    def get_queryset(self) -> QuerySet[Any]:
        if self.request.user.is_anonymous:
            return
        queryset = Category.objects.filter(author=self.request.user).prefetch_related(
            'payments').annotate(payment_sum=Sum('payments__sum'))
        return queryset
    

class CategoryAddView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'category_add.html')
    def post(self, request, *args, **kwargs):
        name = request.POST.get('category')
        category = Category(name=name, author=request.user)
        category.save()
        return redirect('home')