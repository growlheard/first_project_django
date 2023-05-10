from django import forms


class FeedbackForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    phone = forms.EmailField(label='Ваш телефон', max_length=100)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)
