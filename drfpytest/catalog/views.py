from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from drfpytest.catalog.models import Product
from drfpytest.catalog.models import ProductCategory
from drfpytest.catalog.serializers import ProductCategorySerializer
from drfpytest.catalog.serializers import ProductSerializer


class ProductCategories(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def get_queryset(self) -> QuerySet[ProductCategory]:
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            qs = qs.filter(published=True)
        return qs


class Products(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
