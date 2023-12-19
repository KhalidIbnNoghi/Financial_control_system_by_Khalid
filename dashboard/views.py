from typing import Any
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from datetime import date
from .forms import UserRegistrationForm
from dashboard.models import Category, Payment


class HomePageView(LoginRequiredMixin ,ListView):
    login_url = "/login/"
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


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


def logout_user(request):
    logout(request)
    return redirect('home')
