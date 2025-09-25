from django.urls import path
from .views import (
    PrestadorProfileView,
    ImagenGaleriaView,
    ImagenGaleriaDetailView,
    DocumentoLegalizacionView,
    DocumentoLegalizacionDetailView,
    PublicacionListView,
    PublicacionDetailView,
    ConsejoConsultivoListView,
)

urlpatterns = [
    # --- Vistas Privadas (Requieren Autenticación) ---
    path('profile/', PrestadorProfileView.as_view(), name='prestador-profile'),
    path('galeria/', ImagenGaleriaView.as_view(), name='galeria-list-create'),
    path('galeria/<int:pk>/', ImagenGaleriaDetailView.as_view(), name='galeria-detail'),
    path('documentos/', DocumentoLegalizacionView.as_view(), name='documentos-list-create'),
    path('documentos/<int:pk>/', DocumentoLegalizacionDetailView.as_view(), name='documentos-detail'),

    # --- Vistas Públicas ---
    path('publicaciones/', PublicacionListView.as_view(), name='publicaciones-list'),
    path('publicaciones/<slug:slug>/', PublicacionDetailView.as_view(), name='publicaciones-detail'),
    path('consejo-consultivo/', ConsejoConsultivoListView.as_view(), name='consejo-consultivo-list'),
]