from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .models import PrestadorServicio, ImagenGaleria, DocumentoLegalizacion, Publicacion, ConsejoConsultivo
from .serializers import (
    PrestadorServicioSerializer,
    ImagenGaleriaSerializer,
    DocumentoLegalizacionSerializer,
    PublicacionListSerializer,
    PublicacionDetailSerializer,
    ConsejoConsultivoSerializer,
)

class PrestadorProfileView(generics.RetrieveUpdateAPIView):
    """
    Vista para que un prestador de servicios vea y actualice su perfil.
    - GET: Devuelve el perfil del prestador autenticado.
    - PUT/PATCH: Actualiza el perfil del prestador autenticado.
    """
    queryset = PrestadorServicio.objects.all()
    serializer_class = PrestadorServicioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Sobrescribimos este método para devolver siempre el perfil
        del usuario que realiza la petición.
        Esto asegura que un prestador solo pueda ver y editar su propio perfil.
        """
        # Intentamos obtener el perfil del usuario logueado.
        # El bloque try-except maneja el caso (muy improbable si el registro funciona bien)
        # de que un usuario autenticado no tenga un perfil de prestador.
        try:
            return self.request.user.perfil_prestador
        except PrestadorServicio.DoesNotExist:
            # En un caso real, aquí se podría registrar el error o lanzar una excepción más específica.
            # Por ahora, devolvemos un 404, que es lo que haría el comportamiento por defecto.
            from django.http import Http404
            raise Http404("El perfil de prestador no fue encontrado para este usuario.")


class ImagenGaleriaView(generics.ListCreateAPIView):
    """
    Vista para listar y subir imágenes a la galería del prestador autenticado.
    """
    serializer_class = ImagenGaleriaSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """Devuelve solo las imágenes del prestador que hace la petición."""
        return ImagenGaleria.objects.filter(prestador=self.request.user.perfil_prestador)

    def perform_create(self, serializer):
        """Asocia la nueva imagen con el perfil del prestador que la sube."""
        serializer.save(prestador=self.request.user.perfil_prestador)


class ImagenGaleriaDetailView(generics.RetrieveDestroyAPIView):
    """
    Vista para ver y eliminar una imagen específica de la galería.
    """
    serializer_class = ImagenGaleriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Asegura que solo se puedan borrar imágenes del propio prestador."""
        return ImagenGaleria.objects.filter(prestador=self.request.user.perfil_prestador)


class DocumentoLegalizacionView(generics.ListCreateAPIView):
    """
    Vista para listar y subir documentos de legalización del prestador autenticado.
    """
    serializer_class = DocumentoLegalizacionSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """Devuelve solo los documentos del prestador que hace la petición."""
        return DocumentoLegalizacion.objects.filter(prestador=self.request.user.perfil_prestador)

    def perform_create(self, serializer):
        """Asocia el nuevo documento con el perfil del prestador que lo sube."""
        serializer.save(prestador=self.request.user.perfil_prestador)


class DocumentoLegalizacionDetailView(generics.RetrieveDestroyAPIView):
    """
    Vista para ver y eliminar un documento específico de legalización.
    """
    serializer_class = DocumentoLegalizacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Asegura que solo se puedan borrar documentos del propio prestador."""
        return DocumentoLegalizacion.objects.filter(prestador=self.request.user.perfil_prestador)


# --- Vistas Públicas ---

class PublicacionListView(generics.ListAPIView):
    """
    Vista pública para listar todas las publicaciones (eventos, noticias, etc.).
    Permite filtrar por tipo, por ejemplo: /api/publicaciones/?tipo=EVENTO
    """
    serializer_class = PublicacionListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Filtra para mostrar solo las publicaciones marcadas como 'publicadas'.
        También filtra por el 'tipo' si se pasa como parámetro en la URL.
        Permite múltiples tipos separados por comas. Ej: ?tipo=EVENTO,CAPACITACION
        """
        queryset = Publicacion.objects.filter(es_publicado=True)
        tipos = self.request.query_params.get('tipo', None)
        if tipos:
            # Separamos los tipos por comas, eliminamos espacios y los ponemos en mayúsculas
            lista_tipos = [tipo.strip().upper() for tipo in tipos.split(',')]
            queryset = queryset.filter(tipo__in=lista_tipos)
        return queryset


class PublicacionDetailView(generics.RetrieveAPIView):
    """
    Vista pública para ver el detalle de una publicación específica por su slug.
    """
    serializer_class = PublicacionDetailSerializer
    permission_classes = [AllowAny]
    queryset = Publicacion.objects.filter(es_publicado=True)
    lookup_field = 'slug'  # Usa el slug en lugar del ID para la URL


class ConsejoConsultivoListView(generics.ListAPIView):
    """
    Vista pública para listar todas las publicaciones del Consejo Consultivo.
    """
    queryset = ConsejoConsultivo.objects.all().order_by('-fecha_publicacion')
    serializer_class = ConsejoConsultivoSerializer
    permission_classes = [AllowAny]