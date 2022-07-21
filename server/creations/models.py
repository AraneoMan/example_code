from django.db import models, IntegrityError
from django.utils import timezone

from accounts.models import User
from utils.constants import DEFAULT_SECURITY_DOCUMENT_NUMBER
from utils.models import AbstractCreatedUpdatedModel


class CreationType(models.Model):
    """
    Тип Творения
    """
    title = models.CharField('Название', max_length=127)
    title_en = models.CharField('Название на английском', max_length=127)
    parent = models.ForeignKey('CreationType', verbose_name='Заголовок', related_name='subtitles',
                               on_delete=models.PROTECT, null=True)
    position = models.PositiveSmallIntegerField('Позиция в списке', default=0)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Тип Творения'
        verbose_name_plural = 'Типы Творений'
        ordering = ('-position',)

    def __str__(self):
        title = self.title
        if self.parent:
            title = f'{self.parent.title} - {self.title}'
        return title


class Creation(AbstractCreatedUpdatedModel):
    """
    Творение (Результат Интеллектуальной Деятельности)
    """
    NOT_CONFIRMED_STATUS = 'not_confirmed'
    IN_PROGRESS_STATUS = 'in_progress'
    PROTECTED_STATUS = 'protected'
    STATUS_CHOICES = (
       (NOT_CONFIRMED_STATUS, 'Не подтверждено'),
       (IN_PROGRESS_STATUS, 'В процессе'),
       (PROTECTED_STATUS, 'Защищен'),
    )

    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='creations', on_delete=models.PROTECT)
    title = models.TextField('Название')
    title_en = models.TextField('Название на английском', null=True)
    type = models.ForeignKey(CreationType, verbose_name='Тип', on_delete=models.PROTECT)
    status = models.CharField('Статус', max_length=63, choices=STATUS_CHOICES, default=NOT_CONFIRMED_STATUS)
    protected_at = models.DateTimeField('Дата защиты', null=True)
    certificate_number = models.PositiveIntegerField('Номер свидетельства', unique=True, db_index=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Творение (РИД)'
        verbose_name_plural = 'Творения (РИД)'

    def __str__(self):
        return f'{self.title} ({self.status})'

    def save(self, tries=0, **kwargs):
        if not self.id:
            highest_number = Creation.objects.aggregate(models.Max('certificate_number'))['certificate_number__max']
            if not highest_number or highest_number < DEFAULT_SECURITY_DOCUMENT_NUMBER:
                self.certificate_number = DEFAULT_SECURITY_DOCUMENT_NUMBER
            else:
                self.certificate_number = highest_number + 1

        try:
            super().save(**kwargs)
        except IntegrityError as ex:
            if self.id or tries > 4:
                raise ex
            self.save(tries=tries+1, **kwargs)

    def set_protected(self):
        self.status = self.PROTECTED_STATUS
        self.protected_at = timezone.now()
        self.save(update_fields=('status', 'protected_at'))


class CreationFile(AbstractCreatedUpdatedModel):
    """
    Файл Творения
    """
    SOURCE_FILE = 'source_file'
    SIGNATURE_FILE = 'signature_file'
    FILE_TYPE_CHOICES = (
        (SOURCE_FILE, 'Исходник'),
        (SIGNATURE_FILE, 'Цифровая подпись'),
    )

    YANDEX_DISK = 'yandex_disk'
    GOOGLE_DRIVE = 'google_drive'
    INNER_STORAGE = 'inner_storage'
    S3_STORAGE = 's3_storage'
    STORAGE_TYPE_CHOICES = (
        (YANDEX_DISK, 'Яндекс Диск'),
        (GOOGLE_DRIVE, 'Google Диск'),
        (INNER_STORAGE, 'Внутреннее хранилище'),
        (S3_STORAGE, 'AWS S3 хранилище'),
    )

    creation = models.ForeignKey(Creation, verbose_name='Творение', related_name='files',
                                 on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='creations_files',
                             on_delete=models.PROTECT)
    file_type = models.CharField('Тип файла', max_length=63, choices=FILE_TYPE_CHOICES)
    storage_type = models.CharField('Тип хранилища', max_length=63, choices=STORAGE_TYPE_CHOICES)

    file_name = models.CharField('Имя файла', max_length=255)
    file_size = models.BigIntegerField('Размер файла', null=True)
    check_sum = models.CharField('Контрольная сумма', max_length=255, null=True)  # берем MD5 hash
    file_identifier = models.TextField('Идентификатор файла')  # что бы найти в хранилище

    objects = models.Manager()

    class Meta:
        verbose_name = 'Файл Творения'
        verbose_name_plural = 'Файлы Творений'

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self.creation.user_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Творение #{self.creation_id} - {self.file_type} ({self.storage_type})'
