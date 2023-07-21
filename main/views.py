from django.shortcuts import render, get_object_or_404
from django.core.signing import BadSignature

from .models import Service, SimpleUser
from .forms import ChangeUserInfoForm, RegisterUserForm
from .utilities import signer

from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, \
    PasswordResetView, PasswordResetConfirmView, TemplateView

from django.views.generic.edit import UpdateView, CreateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy


###########################################################


def index(request):
    """Главная"""
    return render(request, 'main/index.html')


def contancts(request):
    """Контакты"""
    return render(request, 'main/contacts.html')


def services(request):
    """Услуги"""
    services = Service.objects.all()
    return render(request, 'main/services.html', {'services': services})


# Если юзер авторизован - в шапке он увидит ссылку на профиль
@login_required
def profile(request):
    """Профиль"""
    return render(request, 'main/profile.html')


def user_activate(request, sign):
    """Активация пользователя с сохранением его статуса в базу данных"""
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(SimpleUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class RegisterUserView(CreateView):
    """Контроллер, использующий форму для регистрации"""
    model = SimpleUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView):
    """После регистрации переход на страницу-уведомление"""
    template_name = 'main/register_done.html'


# Классы, осуществляющие Вход и Выход в аккаунт

class UserLoginView(LoginView, LoginRequiredMixin):
    """Login"""
    template_name = 'main/login.html'


class UserLogoutView(LogoutView):
    """Logout"""
    template_name = 'main/logout.html'


# Классы, осуществляющие изменение Профиля и Пароля

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Изменение профиля юзера"""

    model = SimpleUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные успешно изменены.'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                             PasswordChangeView):
    """Изменение пароля юзера"""

    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'


# Классы, осуществляющие сброс пароля юзера

class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    """Отправка письма со ссылкой на сброс пароля на email"""
    template_name = 'main/password_reset.html'
    subject_template_name = 'email/reset_pass_subject.html'
    email_template_name = 'email/reset_pass_body.html'
    success_url = reverse_lazy('main:login')
    success_message = 'Письмо со ссылкой на сброс пароля отправлено на Вашу почту.'


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """Изменение пароля осуществляется этим контроллером"""
    template_name = 'main/confirm_password.html'
    post_reset_login = False
    success_url = reverse_lazy('main:login')
    success_message = 'Ваш пароль успешно изменен'



