from django.shortcuts import render
from .form import FeedbackForm


def home(request):
    return render(request, 'home.html')


def contact(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            return render(request, 'catalog/contact.html', {'success': True})
        print('Запись получена')
    else:
        form = FeedbackForm()
    return render(request, 'catalog/contact.html', {'form': form, 'success': False})
