from rest_framework.exceptions import ParseError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from creations.models import CreationType
from creations.serializers import CreationParentTypeSerializer, CreationCreateSerializer


class CreationTypeListAPIView(ListAPIView):
    """
    Список типов Творения (РИД). Ели выбрать "дочерний" тип,
    то в сертификате будет указаны и тип и подтип.
    """
    serializer_class = CreationParentTypeSerializer

    def get_queryset(self):
        return CreationType.objects.filter(parent__isnull=True)


class CreationCreateAPIView(CreateAPIView):
    """
    Создание Творения (РИД)
    """
    serializer_class = CreationCreateSerializer


class CreationFileUploadAPIView(APIView):
    """
    Загрузка файла Творения (РИД)
    """
    parser_classes = (FileUploadParser,)

    def put(self, request, creation_id, filename):
        file_obj = request.FILES.get('file')
        if not file_obj:
            raise ParseError('нет файла')

        print(file_obj.__dict__)
        # на этом пока все ...

        return Response(status=HTTP_201_CREATED)
