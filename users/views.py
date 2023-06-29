from django.conf import settings

from django.core.mail import send_mail, EmailMessage
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import CreateView, UpdateView, FormView, TemplateView

from users.forms import UserRegisterForm, UserProfileForm, UserPasswordResetForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        subject = 'Верификация учетной записи'
        message = f'Здравствуйте {user.first_name}, пожалуйста проверьте свою учетную запись, перейдя по этой ссылке: ' \
                  f'http://localhost:8000{reverse_lazy("users:confirm_registration", kwargs={"token": user.token})}.'
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.content_subtype = 'html'
        email.send(fail_silently=False)
        return response


class ConfirmRegistrationView(View):
    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        user = User.objects.filter(token=token).first()
        if user:
            user.is_active = True
            user.save()
            return redirect('users:login')
        else:
            return redirect('catalog:home')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordResetView(FormView):
    template_name = 'users/password_reset.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')

    def form_valid(self, form):
        new_password = get_random_string(length=10)
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        subject = 'Сброс пароля'
        message = f'Ваш новый пароль: {new_password}'
        from_email = 'ultrabob@inbox.ru'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        # передача переменной form_submitted в шаблон
        context = self.get_context_data(form=form)
        context['form_submitted'] = True
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_submitted'] = self.request.GET.get('form_submitted', False)
        return context

