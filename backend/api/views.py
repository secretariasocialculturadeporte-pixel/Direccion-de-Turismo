from rest_framework import generics, views, viewsets
from rest_framework.response import Response
from rest_framework import generics, views, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter, OrderingFilter
from dj_rest_auth.registration.views import RegisterView
from .models import (
    PrestadorServicio, ImagenGaleria, DocumentoLegalizacion, Publicacion,
    ConsejoConsultivo, AtractivoTuristico, ElementoGuardado, CategoriaPrestador, Video,
    ContenidoMunicipio
)
from .serializers import (
    PrestadorServicioSerializer,
    ImagenGaleriaSerializer,
    DocumentoLegalizacionSerializer,
    PublicacionListSerializer,
    PublicacionDetailSerializer,
    VideoSerializer,
    ConsejoConsultivoSerializer,
    AtractivoTuristicoListSerializer,
    AtractivoTuristicoDetailSerializer,
    LocationSerializer,
    TuristaRegisterSerializer,
    ElementoGuardadoSerializer,
    ElementoGuardadoCreateSerializer,
    CategoriaPrestadorSerializer,
    PrestadorServicioPublicListSerializer,
    PrestadorServicioPublicDetailSerializer,
    AdminPrestadorServicioSerializer,
    ContenidoMunicipioSerializer,
)
from .permissions import IsTurista, IsAdminOrFuncionario

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


class TuristaRegisterView(RegisterView):
    """
    Vista para el registro de usuarios con el rol de Turista.
    """
    serializer_class = TuristaRegisterSerializer


class ElementoGuardadoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para que los turistas gestionen sus elementos guardados (Mi Viaje).
    Permite listar, crear y eliminar elementos guardados.
    """
    permission_classes = [IsAuthenticated, IsTurista]

    def get_queryset(self):
        # Asegura que cada turista solo pueda ver y gestionar sus propios elementos guardados.
        return ElementoGuardado.objects.filter(usuario=self.request.user)

    def get_serializer_class(self):
        # Usa un serializador diferente para la creación (más simple) vs. la lectura (más detallado).
        if self.action == 'create':
            return ElementoGuardadoCreateSerializer
        return ElementoGuardadoSerializer

    def get_serializer_context(self):
        # Pasa el objeto 'request' al serializador para que pueda acceder al usuario.
        return {'request': self.request}


# --- Vistas Públicas ---

class PublicacionListView(generics.ListAPIView):
    """
    Vista pública para listar todas las publicaciones (eventos, noticias, etc.).
    Permite filtrar por tipo, buscar por texto y ordenar los resultados.
    """
    serializer_class = PublicacionListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['titulo', 'contenido']
    ordering_fields = ['fecha_publicacion', 'titulo']

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


class VideoListView(generics.ListAPIView):
    """
    Vista pública para listar todos los videos.
    """
    queryset = Video.objects.all().order_by('-fecha_publicacion')
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]


class CategoriaPrestadorListView(generics.ListAPIView):
    """
    Vista pública para listar todas las categorías de prestadores de servicios.
    """
    queryset = CategoriaPrestador.objects.all().order_by('nombre')
    serializer_class = CategoriaPrestadorSerializer
    permission_classes = [AllowAny]


class PrestadorServicioPublicListView(generics.ListAPIView):
    """
    Vista pública para listar todos los prestadores de servicios aprobados.
    Permite filtrar por slug de categoría. Ej: /api/prestadores/?categoria=hoteles
    """
    serializer_class = PrestadorServicioPublicListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre_negocio', 'descripcion']
    ordering_fields = ['nombre_negocio']

    def get_queryset(self):
        """
        Filtra para mostrar solo los prestadores aprobados.
        También filtra por 'categoria' si se pasa el slug como parámetro en la URL.
        """
        queryset = PrestadorServicio.objects.filter(aprobado=True)
        categoria_slug = self.request.query_params.get('categoria', None)
        if categoria_slug:
            queryset = queryset.filter(categoria__slug=categoria_slug)
        return queryset


class PrestadorServicioPublicDetailView(generics.RetrieveAPIView):
    """
    Vista pública para ver el detalle de un prestador de servicios por su ID.
    """
    queryset = PrestadorServicio.objects.filter(aprobado=True)
    serializer_class = PrestadorServicioPublicDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'


class AtractivoTuristicoListView(generics.ListAPIView):
    """
    Vista pública para listar todos los atractivos turísticos.
    Permite filtrar por categoria_color. Ej: /api/atractivos/?categoria=AMARILLO
    """
    serializer_class = AtractivoTuristicoListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = AtractivoTuristico.objects.filter(es_publicado=True)
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(categoria_color__iexact=categoria)
        return queryset


class AtractivoTuristicoDetailView(generics.RetrieveAPIView):
    """
    Vista pública para ver el detalle de un atractivo turístico por su slug.
    """
    queryset = AtractivoTuristico.objects.filter(es_publicado=True)
    serializer_class = AtractivoTuristicoDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class LocationListView(views.APIView):
    """
    Vista pública para obtener una lista unificada de todas las ubicaciones
    geográficas (Prestadores y Atractivos) para el mapa interactivo.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        locations = []

        # 1. Obtener Prestadores de Servicio (solo los aprobados y con ubicación)
        prestadores = PrestadorServicio.objects.filter(
            aprobado=True,
            ubicacion_mapa__isnull=False
        ).exclude(ubicacion_mapa__exact='')

        for p in prestadores:
            try:
                # Asumimos que las coordenadas están en formato "lat,lng"
                lat, lng = map(float, p.ubicacion_mapa.split(','))
                locations.append({
                    'id': f'prestador_{p.id}',
                    'nombre': p.nombre_negocio,
                    'lat': lat,
                    'lng': lng,
                    'tipo': p.categoria.slug if p.categoria else 'prestador',
                    # No tenemos página de detalle para prestador aún, así que no se añade URL
                    'url_detalle': None
                })
            except (ValueError, AttributeError):
                # Ignorar si el formato de coordenadas es incorrecto o si no hay categoría
                continue

        # 2. Obtener Atractivos Turísticos (solo los publicados y con ubicación)
        atractivos = AtractivoTuristico.objects.filter(
            es_publicado=True,
            ubicacion_mapa__isnull=False
        ).exclude(ubicacion_mapa__exact='')

        for a in atractivos:
            try:
                lat, lng = map(float, a.ubicacion_mapa.split(','))
                locations.append({
                    'id': f'atractivo_{a.id}',
                    'nombre': a.nombre,
                    'lat': lat,
                    'lng': lng,
                    'tipo': f'atractivo_{a.categoria_color.lower()}',
                    'url_detalle': f'/atractivos/{a.slug}'
                })
            except (ValueError, AttributeError):
                continue

        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)


# --- Vistas de Administración ---

class AdminPrestadorListView(generics.ListAPIView):
    """
    Vista para que el administrador/funcionario vea todos los prestadores.
    Permite filtrar por estado de aprobación. Ej: /api/admin/prestadores/?aprobado=false
    """
    queryset = PrestadorServicio.objects.all().order_by('-fecha_creacion')
    serializer_class = AdminPrestadorServicioSerializer
    permission_classes = [IsAdminOrFuncionario]
    filter_backends = [OrderingFilter]
    ordering_fields = ['fecha_creacion', 'nombre_negocio']

    def get_queryset(self):
        """
        Filtra por el estado de aprobación si se provee el parámetro en la URL.
        """
        queryset = super().get_queryset()
        aprobado_param = self.request.query_params.get('aprobado')
        if aprobado_param is not None:
            # Convertimos el string 'true'/'false' a booleano
            aprobado = aprobado_param.lower() == 'true'
            queryset = queryset.filter(aprobado=aprobado)
        return queryset


class AdminApprovePrestadorView(views.APIView):
    """
    Vista para que un administrador/funcionario apruebe un prestador de servicios.
    """
    permission_classes = [IsAdminOrFuncionario]

    def patch(self, request, pk, *args, **kwargs):
        """
        Maneja la acción de aprobación.
        """
        try:
            prestador = PrestadorServicio.objects.get(pk=pk)
        except PrestadorServicio.DoesNotExist:
            return Response({'error': 'Prestador no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        prestador.aprobado = True
        prestador.save(update_fields=['aprobado'])
        return Response({'status': 'Prestador aprobado con éxito.'}, status=status.HTTP_200_OK)

class ContenidoMunicipioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar el contenido general del municipio.
    - Lectura (list, retrieve) es pública.
    - Escritura (create, update, destroy) es solo para Admins/Funcionarios.
    """
    queryset = ContenidoMunicipio.objects.all().order_by('orden')
    serializer_class = ContenidoMunicipioSerializer

    def get_permissions(self):
        """
        Asigna permisos basados en la acción.
        """
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminOrFuncionario]
        return super().get_permissions()

    def get_serializer_context(self):
        """
        Pasa el request al serializador para que pueda acceder al usuario.
        """
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


# --- Vista para el Sistema de Agentes ---

from .serializers import AgentCommandSerializer

class AgentCommandView(views.APIView):
    """
    Endpoint para recibir y procesar comandos para el sistema de agentes jerárquicos.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Recibe una orden en lenguaje natural, la valida y la pasa al Coronel de Turismo.
        """
        # --- Carga Perezosa (Lazy Loading) de los Agentes ---
        # Los componentes pesados del agente se importan aquí, solo cuando el endpoint es llamado,
        # para no ralentizar el arranque del servidor.
        from agents.corps.turismo_coronel import get_turismo_coronel_graph
        import asyncio

        serializer = AgentCommandSerializer(data=request.data)
        if serializer.is_valid():
            orden = serializer.validated_data['orden']

            # La lógica del agente se ejecuta aquí.
            coronel_agent = get_turismo_coronel_graph()

            # Creamos una configuración única para esta conversación para evitar estados compartidos.
            config = {"configurable": {"thread_id": f"user_command_{request.user.id}"}}

            try:
                # Invocamos el grafo del Coronel de forma asíncrona desde nuestro contexto síncrono.
                result = asyncio.run(coronel_agent.ainvoke({
                    "general_order": orden,
                    "app_context": None
                }, config=config))

                final_report = result.get("final_report", "El agente completó la misión pero no generó un informe final.")
                return Response({"respuesta": final_report}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(
                    {"error": f"Error crítico al procesar la orden con el agente: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)