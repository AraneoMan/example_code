from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.serializers import UserRegistrationSerializer
from accounts.services import ProcessNewUserService, ProcessNewUserException


class RegistrationAPIView(CreateAPIView):
    """
    Регистрация нового пользователя (доступно без токена)
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer


@swagger_auto_schema(method='GET', responses={202: 'Успешно', 400: 'Неверный код подтверждения'},
                     operation_description='Подтверждение email пользователя (доступно без токена)')
@api_view(('GET',))
@permission_classes((AllowAny,))
def confirm_email_view(request, confirm_code: str):
    try:
        ProcessNewUserService.process_confirm_code(confirm_code)
    except ProcessNewUserException:
        raise ValidationError('Неверный код подтверждения')

    return Response('Email Успешно подтвержден', status=status.HTTP_202_ACCEPTED)
