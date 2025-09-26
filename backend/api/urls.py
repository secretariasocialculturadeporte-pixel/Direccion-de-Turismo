from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PrestadorProfileView,
    ImagenGaleriaView,
    ImagenGaleriaDetailView,
    DocumentoLegalizacionView,
    DocumentoLegalizacionDetailView,
    PublicacionListView,
    PublicacionDetailView,
    ConsejoConsultivoListView,
    AtractivoTuristicoListView,
    AtractivoTuristicoDetailView,
    LocationListView,
    ElementoGuardadoViewSet,
    VideoListView,
    CategoriaPrestadorListView,
    PrestadorServicioPublicListView,
    PrestadorServicioPublicDetailView,
    ContenidoMunicipioViewSet,
    AgentCommandView,
)

# Creamos un router para registrar los ViewSets
router = DefaultRouter()
router.register(r'mi-viaje', ElementoGuardadoViewSet, basename='elemento-guardado')

urlpatterns = [
    # --- Vistas Privadas (Requieren Autenticación) ---
    path('profile/', PrestadorProfileView.as_view(), name='prestador-profile'),
    path('galeria/', ImagenGaleriaView.as_view(), name='galeria-list-create'),
    path('galeria/<int:pk>/', ImagenGaleriaDetailView.as_view(), name='galeria-detail'),
    path('documentos/', DocumentoLegalizacionView.as_view(), name='documentos-list-create'),
    path('documentos/<int:pk>/', DocumentoLegalizacionDetailView.as_view(), name='documentos-detail'),
    # Incluimos las rutas del ViewSet de "Mi Viaje"
    path('', include(router.urls)),

    # --- Vistas Públicas ---
    path('prestadores/categorias/', CategoriaPrestadorListView.as_view(), name='prestador-categorias-list'),
    path('prestadores/', PrestadorServicioPublicListView.as_view(), name='prestador-public-list'),
    path('prestadores/<int:pk>/', PrestadorServicioPublicDetailView.as_view(), name='prestador-public-detail'),
    path('publicaciones/', PublicacionListView.as_view(), name='publicaciones-list'),
    path('publicaciones/<slug:slug>/', PublicacionDetailView.as_view(), name='publicaciones-detail'),
    path('consejo-consultivo/', ConsejoConsultivoListView.as_view(), name='consejo-consultivo-list'),
    path('videos/', VideoListView.as_view(), name='videos-list'),
    path('atractivos/', AtractivoTuristicoListView.as_view(), name='atractivos-list'),
    path('atractivos/<slug:slug>/', AtractivoTuristicoDetailView.as_view(), name='atractivos-detail'),
    path('locations/', LocationListView.as_view(), name='locations-list'),
    path('contenido-municipio/', ContenidoMunicipioViewSet.as_view({'get': 'list'}), name='contenido-municipio-public-list'),

    # --- Vistas para el Sistema de Agentes ---
    path('agente/comando/', AgentCommandView.as_view(), name='agent-command'),
]