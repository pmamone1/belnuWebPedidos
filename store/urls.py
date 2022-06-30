from django.urls import path
from . import views
from .api import VariationApiView

urlpatterns = [
    path('', views.store, name="store"),
    path('category/<slug:category_slug>/', views.store, name='product_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('buscar_titulo/<int:product>/<int:edicion>/',VariationApiView.as_view(),name="variation_api"), # url para ajax de buscar titulo + edicion
    path('get/ajax/titulo/', VariationApiView.as_view() , name = "get_ajax_titulo"), # url para ajax de buscar titulo
]
