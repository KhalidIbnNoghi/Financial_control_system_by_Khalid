from typing import Any
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, DetailView
from datetime import date

from dashboard.models import Category, Payment

class HomePageView(ListView):
    template_name = 'index.html'
    context_object_name = 'categories'

    def get_queryset(self) -> QuerySet[Any]:
        if self.request.user.is_anonymous:
            return
        queryset = Category.objects.filter(author=self.request.user).prefetch_related(
            'payments').annotate(payment_sum=Sum('payments__sum'))
        return queryset
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        total_sum = Category.objects.filter(author=self.request.user).aggregate(total_sum=Sum('payments__sum'))['total_sum']
        context['total_sum'] = total_sum

        payment_history = Payment.objects.filter(category__author=self.request.user).values('category', 'sum', 'date')
        context['payment_history'] = payment_history

        return context


class CategoryAddView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'category_add.html')
    def post(self, request, *args, **kwargs):
        name = request.POST.get('category')
        category = Category(name=name, author=request.user)
        category.save()
        return redirect('home')


class PaymentAddView(DetailView):
    model = Category
    template_name = 'payment_add.html'

    def post(self, request, *args, **kwargs):
        sum = request.POST.get('sum')
        payment = Payment(sum=sum, category_id=kwargs.get('pk'), date = str(date.today()))
        payment.save()
        return redirect('home')
