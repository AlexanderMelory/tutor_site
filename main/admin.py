from django.contrib import admin
import datetime

from .models import Service, SimpleUser

from .utilities import send_activation_notification


def send_activation_notifications(modeladmin, request, queryset):
    """Отправка писем администратором к неактивированным юзерам"""

    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с требованиями отправлены')


send_activation_notifications.short_description = \
    'Отправка писем с требованиями активации'


class NoactivatedFilter(admin.SimpleListFilter):
    """Фильтрует активированных юзеров и неактивированных"""

    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('threedays', 'Не прошли более 3 дней'),
            ('week', 'Не прошли более недели'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False,
                                   date_joined_date_lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False,
                                   date_joined_date_lt=d)


class ServiceAdmin(admin.ModelAdmin):
    """Управление Услугами через админ-сайт"""

    list_display = ('title', 'content', 'price', 'image')
    fields = ('title', 'content', 'price', 'image')


class SimpleUserAdmin(admin.ModelAdmin):
    """Управление юзерами через админ-сайт"""

    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NoactivatedFilter,)
    fields = (('username', 'email'), ('first_name', 'last_name'),
              ('send_messages', 'is_active', 'is_activated'),
              ('is_staff', 'is_superuser'),
              'groups', 'user_permissions',
              ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)


admin.site.register(Service, ServiceAdmin)
admin.site.register(SimpleUser, SimpleUserAdmin)
# Register your models here.
