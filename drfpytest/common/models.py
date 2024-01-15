from uuid import uuid4

from django.db import models
from django_pydantic_field import SchemaField


class CommonModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


# noinspection PyPep8Naming
def JSONSchemaField(*args, **kwargs):  # noqa: N802
    kwargs.setdefault('exclude_unset', True)
    return SchemaField(*args, **kwargs)
