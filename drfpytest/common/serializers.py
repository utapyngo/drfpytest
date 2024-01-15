from django_pydantic_field.rest_framework import SchemaField


class JSONSchemaField(SchemaField):
    def __init__(self, **kwargs):
        kwargs.setdefault('exclude_unset', True)
        super().__init__(**kwargs)
