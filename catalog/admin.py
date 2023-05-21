from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product, Category
from .forms import ProductForm, ProductUpdateForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description',)

    # регистрируем функцию редактирования как действие
    def edit_selected(self, request, queryset):
        if queryset.count() == 1:
            obj = queryset.first()
            url = reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name),
                          args=[obj.pk])
            return HttpResponseRedirect(url)
        else:
            self.message_user(request, "Выберите только один объект для редактирования.")

    edit_selected.short_description = "Редактировать выбранный объект"

    # регистрируем действие в админке
    actions = ['edit_selected']

    def get_actions(self, request):
        actions = super(ProductAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # заменяем форму для редактирования объекта на свою собственную
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return ProductForm
        else:
            return ProductUpdateForm
