from django.contrib import admin
from dashboard.models import Category, Payment, Profile


# admin.site.register(Category)
# admin.site.register(Payment)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ( 'name', 'author' )
    list_display = ( 'name', 'author' )
    list_filter = ( 'name', 'author' )
    ordering = ('-name',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    fields = ( 'sum', 'date', 'category' )
    list_display = ( 'sum', 'date', 'category' )
    list_filter = ( 'date', )
    ordering = ('-date',)
