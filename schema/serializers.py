from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import DataSource, Schema, Table, Column
from .util import SQLDatabase


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = "__all__"

    def validate(self, attrs):
        uri = attrs.get("uri", None)
        database = SQLDatabase.from_uri(uri)
        database.get_table_names()
        return super().validate(attrs)


class URISerializer(serializers.Serializer):
    uri = serializers.URLField(write_only=True)


class ColumnProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = "__all__"


class TableProfileSerializer(serializers.ModelSerializer):
    column = serializers.SerializerMethodField("get_column", read_only=True)

    class Meta:
        model = Table
        fields = "__all__"

    def get_columns(self, instance):
        return Column.objects.filter(table=instance).values()


class SchemaProfileSerializer(serializers.ModelSerializer):
    table = serializers.SerializerMethodField("get_tables", read_only=True)

    class Meta:
        model = Schema
        fields = "__all__"

    def get_tables(self, instance):
        return Table.objects.filter(schema=instance).values()


class DataSourceProfileSerializer(serializers.ModelSerializer):
    schema = serializers.SerializerMethodField("get_schemas", read_only=True)

    class Meta:
        model = DataSource

    def get_schemas(self, instance):
        return Schema.objects.filter(datasource=instance).values()
