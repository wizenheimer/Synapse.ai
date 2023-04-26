from django.db import models


class DataSource(models.Model):
    DATASOURCE_OPTIONS = (
        ("PostgreSQL", "PostgreSQL"),
        ("MySQL", "MySQL"),
        ("Oracle", "Oracle"),
        ("SQLite", "SQLite"),
        ("Snowflake", "Snowflake"),
    )
    # display name for the database
    name = models.CharField(max_length=250)
    # uri in sqlalchemy compliant format
    uri = models.URLField()
    category = models.CharField(
        choices=DATASOURCE_OPTIONS, max_length=255, default="Undefined"
    )
    # datasource metadata
    # datasource connection is validated
    is_verified = models.BooleanField(default=False)
    # datasource is enabled for querying
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Schema(models.Model):
    # high level schema
    name = models.CharField(max_length=250)
    datasource = models.ForeignKey(
        DataSource,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="schema",
    )

    def __str__(self):
        return self.name


class Table(models.Model):
    # table schema
    name = models.CharField(max_length=250)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name="table")

    def __str__(self):
        return self.name


class Column(models.Model):
    # column schema
    name = models.CharField(max_length=250)
    data_type = models.CharField(max_length=250)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="column")

    def __str__(self):
        return self.name
