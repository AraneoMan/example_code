from django.conf import settings
from django.core import signing
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import BadSignature
from django.urls import reverse

from accounts.models import User, UserCommunity
from utils.tasks import send_email_task


class ProcessNewUserException(Exception):
    pass


class ProcessNewUserService:
    def __init__(self, user: User):
        self._user = user

    def process(self):
        self._send_confirm_email_code()
        self._create_community()

    @staticmethod
    def process_confirm_code(confirm_code: str):
        try:
            user_id, email = signing.loads(confirm_code.strip())
            user = User.objects.get(id=user_id, email=email)
        except (BadSignature, ObjectDoesNotExist):
            raise ProcessNewUserException

        user.confirm_email = True
        user.save(update_fields=('confirm_email',))

    def _send_confirm_email_code(self):
        confirm_email_code = signing.dumps((self._user.id, self._user.email))
        confirm_email_url = f'{settings.SITE_NAME}' \
                            f'{reverse("accounts:confirm_email", kwargs={"confirm_code": confirm_email_code})}'

        send_email_task.delay(
            subject=f'Завершение регистрации на {settings.SITE_NAME}',
            body_template='accounts/confirm_email_email_body.html',
            context={'confirm_url': confirm_email_url},
            to_email=self._user.email,
        )

    def _create_community(self):
        if hasattr(self._user, 'personal_community'):
            return

        personal_community = UserCommunity.objects.create(owner=self._user)
        for community in self._user.communities.all().select_related('owner'):
            personal_community.participants.add(community.owner)

        personal_community.participants.add(self._user)
