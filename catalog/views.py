from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from .tasks import send_congratulations
from django.views.generic import TemplateView, FormView, DetailView, ListView, CreateView, UpdateView, DeleteView
from .forms import FeedbackForm, PostForm, ProductForm, VersionForm
from .models import Product, Category, Post, Version


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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_create.html'
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_update.html'
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        context_data['versions'] = self.object.version_set.all()

        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:index')


class IndexView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(Prefetch('version_set', queryset=Version.objects.filter(is_active=True)))
        for product in queryset:
            if len(product.description) > 100:
                product.description = product.description[:100] + '...'
        return queryset


class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(is_published=True)
    template_name = 'catalog/post_list.html'
    context_object_name = 'post_list'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'catalog/post_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



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

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'catalog/post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('catalog:post_list')
