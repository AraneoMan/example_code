# Минимальный номер сертификата
DEFAULT_SECURITY_DOCUMENT_NUMBER = 10489734

# Типы событий для логирования в БД
NONE_LOG_EVENT_TYPE = 'unknown'  # заглушка, если не указан тип события. Всегда указывай тип события
EMAIL_DOES_NOT_SEND_EVENT_TYPE = 'email_does_not_send'

LOG_EVENT_TYPE_CHOICES = (
    (NONE_LOG_EVENT_TYPE, 'Неизвестно'),
    (EMAIL_DOES_NOT_SEND_EVENT_TYPE, 'Письмо не отправлено'),
)


# API ошибки `accounts` app
USER_EMAIL_UNIQUE = 'Пользователь с таким Email уже зарегистрирован'
