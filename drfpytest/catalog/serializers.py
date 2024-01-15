from rest_framework import serializers

from drfpytest.catalog.models import Product
from drfpytest.catalog.models import ProductCategory
from drfpytest.catalog.schemas import ProductData
from drfpytest.common.serializers import JSONSchemaField


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    data = JSONSchemaField(schema=ProductData)

    class Meta:
        model = Product
        fields = '__all__'
