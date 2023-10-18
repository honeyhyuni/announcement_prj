from django.core.cache import cache
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response

from company.models import Company
from company.serializers import CompanyListSerializer


# Create your views here.
class CompanyListAPIView(ListCreateAPIView):
    queryset = Company.objects.all().prefetch_related('recruitment_set')
    serializer_class = CompanyListSerializer

    def list(self, request, *args, **kwargs):
        if 'company' in cache:
            return Response(cache.get('company'), status=status.HTTP_200_OK)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        cache.set('company', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
