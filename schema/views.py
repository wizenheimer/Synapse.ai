from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DataSource, Schema, Table, Column
from .serializers import (
    DataSourceSerializer,
    DataSourceProfileSerializer,
    URISerializer,
)


class DataSourceViewset(viewsets.ModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer

    @action(detail=True, methods=["post"])
    def set_uri(self, request, pk=None):
        datasource = DataSource.objects.get(pk=pk)
        serializer = URISerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # to do : validate it by checking if the data query is supported
        datasource.uri = serializer.data["uri"]
        datasource.save()
        return Response({"status": "URI saved successfully."})

    @action(detail=True, methods=["get"])
    def test_uri(self, request, pk=None):
        datasource = DataSource.objects.get(pk=pk)
        # to do : test the current uri
        can_connect = True
        if can_connect:
            return Response({"status": "database connection established."})
        else:
            return Response({"status": "database connection couldn't be established."})

    @action(detail=True, methods=["get"])
    def get_representation(self, request, pk=None):
        datasource = DataSource.objects.get(pk=pk)
        serializer = DataSourceProfileSerializer(datasource, many=True)
        return Response(serializer.data)
