from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminPrestadorListView,
    AdminApprovePrestadorView,
    ContenidoMunicipioViewSet,
)

router = DefaultRouter()
router.register(r'contenido-municipio', ContenidoMunicipioViewSet, basename='contenido-municipio')

urlpatterns = [
    path('prestadores/', AdminPrestadorListView.as_view(), name='admin-prestadores-list'),
    path('prestadores/<int:pk>/approve/', AdminApprovePrestadorView.as_view(), name='admin-prestador-approve'),
    path('', include(router.urls)),
]