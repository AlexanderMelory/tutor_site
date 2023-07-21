from django.db import models
from django.contrib.auth.models import AbstractUser


class SimpleUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Прошел активацию?')

    class Meta(AbstractUser.Meta):
        pass


class Service(models.Model):
    """Класс, описывающий объект-услугу"""

    title = models.CharField(max_length=40, verbose_name='Услуга')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(default=0, verbose_name='Стоимость')

    image = models.ImageField(upload_to='media/', blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Услуги'
        verbose_name = 'Услуга'
