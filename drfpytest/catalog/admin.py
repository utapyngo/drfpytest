from autocompletefilter.admin import AutocompleteFilterMixin
from autocompletefilter.filters import AutocompleteListFilter
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from drfpytest.catalog.models import Product
from drfpytest.catalog.models import ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(AutocompleteFilterMixin, ImportExportModelAdmin):
    autocomplete_fields = ('parent',)
    list_display = ('name', 'parent', 'published')
    list_filter = (
        ('parent', AutocompleteListFilter),
        'published',
    )
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    autocomplete_fields = ('category',)
    list_display = ('article', 'name', 'category')
    list_filter = (('category', AutocompleteListFilter),)
    search_fields = ('article', 'name')
