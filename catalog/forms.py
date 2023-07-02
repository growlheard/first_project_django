from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django import forms
from .models import Product, Post, Version


class FeedbackForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    phone = forms.EmailField(label='Ваш телефон', max_length=100)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить', css_class='btn-success'))

    class Meta:
        model = Product
        exclude = ('owner',)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']

        if name and any(word in name.lower() for word in forbidden_words):
            self.add_error('name', 'Недопустимое слово в названии продукта.')

        if description and any(word in description.lower() for word in forbidden_words):
            self.add_error('description', 'Недопустимое слово в описании продукта.')


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()


class PostForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить', css_class='btn-success'))

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('owner',)
