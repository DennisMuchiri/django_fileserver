from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from rest_framework import generics, viewsets, serializers, filters, status
from apps.authentication.models import CustomUser
from django.db.models import Q
from django.core import serializers
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import logging


from apps.setup.models import MyFile
from apps.setup.serializers import MyFileSerializer

logger = logging.getLogger(__name__)


class MyFileViewSet(viewsets.ModelViewSet):
    queryset = MyFile.objects.all()
    serializer_class = MyFileSerializer
    filter_backends = [DjangoFilterBackend]

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = MyFile.objects.all()
        return qs

    obj_name = 'my_file'

    def get_serializer_class(self):
        return MyFileSerializer