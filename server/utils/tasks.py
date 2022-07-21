import logging

from celery.schedules import crontab
from django.core.mail import EmailMessage
from django.template import loader
from django.utils import timezone

from core import settings
from core.celery import app
from utils.constants import EMAIL_DOES_NOT_SEND_EVENT_TYPE

database_logger = logging.getLogger('database_logger')


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=2, minute=3),
        delete_old_logs_task.s()
    )


@app.task
def delete_old_logs_task():
    from utils.models import Log

    past_time = timezone.now() - timezone.timedelta(days=10)
    Log.objects.filter(created__lt=past_time).delete()


@app.task
def send_email_task(subject: str, body_template: str, context: dict | None, to_email: str | list[str] | tuple[str],
                    from_email: str = None):
    body = loader.render_to_string(body_template, context)
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    if isinstance(to_email, str):
        to_email = (to_email,)

    email = EmailMessage(subject, body, from_email, to_email)
    count = email.send()
    if count < len(to_email):
        database_logger.error('Письмо не отправлено', extra={
            'event_type': EMAIL_DOES_NOT_SEND_EVENT_TYPE,
            'extra': {'subject': subject, 'to_email': to_email}
        })
