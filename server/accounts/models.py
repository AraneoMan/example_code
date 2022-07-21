from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('full_name', )

    username = None
    first_name = None
    last_name = None

    email = models.EmailField('Email адрес', unique=True, db_index=True)
    full_name = models.CharField('ФИО', max_length=255)
    full_name_en = models.CharField('ФИО на английском', max_length=255, blank=True, null=True)
    phone_number = models.CharField('Телефон', max_length=30, null=True)

    confirm_email = models.BooleanField('Email подтвержден', default=False)

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self) -> str:
        return str(self.full_name)

    def get_short_name(self) -> str:
        return str(self.full_name)

    def __str__(self):
        return self.email


class UserCommunity(models.Model):
    owner = models.OneToOneField(User, verbose_name='Владелец', related_name='personal_community',
                                 on_delete=models.PROTECT)
    participants = models.ManyToManyField(User, verbose_name='Участники', related_name='communities')

    objects = models.Manager()

    class Meta:
        verbose_name = 'Сообщество пользователя'
        verbose_name_plural = 'Сообщества пользователей'

    def __str__(self):
        return f'Сообщество пользователя {self.owner.email}'
