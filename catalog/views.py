from django.shortcuts import render
from .forms import FeedbackForm
from .models import Product, Category


def home(request):
    latest_products = Product.objects.order_by('created_at')[:5]
    for products in latest_products:
        print(products.name)
    context = {
        'object_list': Product.objects.all(),
        'category_list': Category.objects.all()
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            return render(request, 'catalog/contacts.html', {'success': True})
        print('Запись получена')
    else:
        form = FeedbackForm()
    return render(request, 'catalog/contacts.html', {'form': form, 'success': False})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)


def index(request):
    products = Product.objects.all()

    for product in products:
        if len(product.description) > 100:
            product.description = product.description[:100] + '...'

    context = {'products': products}
    return render(request, 'catalog/index.html', context)
