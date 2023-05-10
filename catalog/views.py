from django.shortcuts import render
from .form import FeedbackForm


def home(request):
    return render(request, 'home.html')


def contacts(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            return render(request, 'catalog/contacts.html', {'success': True})
        print('Запись получена')
    else:
        form = FeedbackForm()
    return render(request, 'catalog/contacts.html', {'form': form, 'success': False})
