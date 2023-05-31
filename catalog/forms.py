from django import forms
from .models import Product, Post


class FeedbackForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    phone = forms.EmailField(label='Ваш телефон', max_length=100)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()


class PostForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Post
        fields = '__all__'
