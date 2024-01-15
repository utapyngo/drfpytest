from django.contrib.postgres.indexes import GinIndex
from django.db import models

from drfpytest.catalog.schemas import ProductData
from drfpytest.common.models import CommonModel
from drfpytest.common.models import JSONSchemaField


class ProductCategory(CommonModel):
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='children'
    )
    name = models.CharField(max_length=255, unique=True)
    published = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'product categories'

    def __str__(self) -> str:
        return self.name


class Product(CommonModel):
    name = models.CharField(max_length=255, db_index=True)
    article = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    category = models.ForeignKey(
        ProductCategory, related_name='products', on_delete=models.SET_NULL, blank=True, null=True
    )
    data: ProductData = JSONSchemaField()

    class Meta:
        indexes = (GinIndex(fields=['data']),)

    def __str__(self) -> str:
        return self.name
