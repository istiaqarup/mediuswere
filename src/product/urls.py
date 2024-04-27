from django.urls import path
from django.views.generic import TemplateView

from product.views.product import CreateProductView, ProductUpdateView,ShowProductList,ProductDetailView, filter_products, product_variants
from product.views.variant import VariantView, VariantCreateView, VariantEditView

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('list/', ShowProductList.as_view(), name='list.product'),
    path('summery/<int:pk>', ProductDetailView.as_view(), name='summery_product'),
    path('filtered-product/', filter_products, name='filtered_product'),
    path('product-varient/', product_variants, name='product-varient'),
    path('update-product/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
]
