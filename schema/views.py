from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DataSource, Schema, Table, Column
from .util import SQLDatabase, SQLAlchemyError
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
        # NOTE : input components and buil url on client side
        datasource.uri = serializer.data["uri"]
        datasource.save()
        return Response({"status": "URI saved successfully."})

    @action(detail=True, methods=["get"])
    def test_uri(self, request, pk=None):
        datasource = DataSource.objects.get(pk=pk)
        # to do : test the current uri
        database = SQLDatabase.from_uri(datasource.uri)
        try:
            database.get_table_names()
        except Exception as e:
            return Response({"status": "database connection couldn't be established."})
        finally:
            return Response({"status": "database connection established."})

    @action(detail=True, methods=["get"])
    def get_representation(self, request, pk=None):
        datasource = DataSource.objects.get(pk=pk)
        serializer = DataSourceProfileSerializer(datasource, many=True)
        return Response(serializer.data)
