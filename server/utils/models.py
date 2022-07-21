from django.db import models

from accounts.models import User
from utils.constants import LOG_EVENT_TYPE_CHOICES


class AbstractCreatedUpdatedModel(models.Model):
    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        abstract = True


class Log(models.Model):
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    LEVEL_CHOICES = (
        (INFO, 'Выполнено'),
        (WARNING, 'Предупреждение'),
        (ERROR, 'Ошибка')
    )

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True)
    level = models.CharField('Статус', max_length=15, choices=LEVEL_CHOICES)
    event_type = models.CharField('Тип события', max_length=63, choices=LOG_EVENT_TYPE_CHOICES)
    message = models.TextField('Сообщение', blank=True, null=True)
    traceback = models.TextField('Трассировка', null=True)
    extra = models.JSONField('Подробности', default=dict)

    created = models.DateTimeField('Создано', auto_now_add=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ['-created']
