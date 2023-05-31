from django.urls import reverse_lazy, reverse
from .tasks import send_congratulations
from django.views.generic import TemplateView, FormView, DetailView, ListView, CreateView, UpdateView, DeleteView
from .forms import FeedbackForm, PostForm
from .models import Product, Category, Post


class HomeView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_products = Product.objects.order_by('created_at')[:5]
        context['object_list'] = Product.objects.all()
        context['category_list'] = Category.objects.all()
        for product in latest_products:
            print(product.name)
        return context


# def home(request):
#   latest_products = Product.objects.order_by('created_at')[:5]
#   for products in latest_products:
#       print(products.name)
#   context = {
#       'object_list': Product.objects.all(),
#       'category_list': Category.objects.all()
#   }
#   return render(request, 'catalog/home.html', context)


class ContactsView(FormView):
    template_name = 'catalog/contacts.html'
    form_class = FeedbackForm
    success_url = '/contacts/?success=True'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, success=False))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        success = self.request.GET.get('success')
        if success:
            context['success'] = True
        else:
            context['success'] = False
        return context


# def contacts(request):
#    if request.method == 'POST':
#        form = FeedbackForm(request.POST)
#        if form.is_valid():
#            return render(request, 'catalog/contacts.html', {'success': True})
#        print('Запись получена')
#    else:
#        form = FeedbackForm()
#    return render(request, 'catalog/contacts.html', {'form': form, 'success': False})
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


# def product_detail(request, pk):
#    product = Product.objects.get(pk=pk)
#    context = {'product': product}
#    return render(request, 'catalog/product_detail.html', context)
class IndexView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        for product in queryset:
            if len(product.description) > 100:
                product.description = product.description[:100] + '...'
        return queryset


# def index(request):
#    products = Product.objects.all()
#
#    for product in products:
#        if len(product.description) > 100:
#            product.description = product.description[:100] + '...'
#
#    context = {'products': products}
#    return render(request, 'catalog/index.html', context)

class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(is_published=True)
    template_name = 'catalog/post_list.html'
    context_object_name = 'post_list'


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'catalog/post_create.html'

    def get_success_url(self):
        obj = self.object
        return reverse('catalog:post_detail', kwargs={'slug': obj.slug})

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.save()
        return response


class PostDetailView(DetailView):
    model = Post
    template_name = 'catalog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views_count += 1
        obj.save()
        if obj.views_count == 100:
            send_congratulations(obj)
        return obj


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'preview', 'content']
    template_name = 'catalog/post_edit.html'
    success_url = reverse_lazy('catalog:post_list')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'catalog/post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('catalog:post_list')
