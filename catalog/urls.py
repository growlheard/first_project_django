from django.urls import path
from .views import HomeView, ContactsView, ProductDetailView, IndexView, PostListView, PostCreateView, PostDetailView, \
    PostUpdateView, PostDeleteView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('index/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('index/', IndexView.as_view(), name='index'),
    path('blog/', PostListView.as_view(), name='post_list'),
    path('blog/post_create/', PostCreateView.as_view(), name='post_create'),
    path('post_detail/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name='post_confirm_delete'),
    path('product_create/', ProductCreateView.as_view(), name='product_create'),
    path('product_update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
]