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
    AgentCommandSerializer,
)
from .permissions import IsTurista, IsAdminOrFuncionario
from asgiref.sync import async_to_sync

class PrestadorProfileView(generics.RetrieveUpdateAPIView):
    """
    Vista para que un prestador de servicios vea y actualice su perfil.
    """
    queryset = PrestadorServicio.objects.all()
    serializer_class = PrestadorServicioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.perfil_prestador
        except PrestadorServicio.DoesNotExist:
            from django.http import Http404
            raise Http404("El perfil de prestador no fue encontrado para este usuario.")


class ImagenGaleriaView(generics.ListCreateAPIView):
    serializer_class = ImagenGaleriaSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ImagenGaleria.objects.filter(prestador=self.request.user.perfil_prestador)

    def perform_create(self, serializer):
        serializer.save(prestador=self.request.user.perfil_prestador)


class ImagenGaleriaDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ImagenGaleriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ImagenGaleria.objects.filter(prestador=self.request.user.perfil_prestador)


class DocumentoLegalizacionView(generics.ListCreateAPIView):
    serializer_class = DocumentoLegalizacionSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return DocumentoLegalizacion.objects.filter(prestador=self.request.user.perfil_prestador)

    def perform_create(self, serializer):
        serializer.save(prestador=self.request.user.perfil_prestador)


class DocumentoLegalizacionDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = DocumentoLegalizacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DocumentoLegalizacion.objects.filter(prestador=self.request.user.perfil_prestador)


class TuristaRegisterView(RegisterView):
    serializer_class = TuristaRegisterSerializer


class ElementoGuardadoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsTurista]

    def get_queryset(self):
        return ElementoGuardado.objects.filter(usuario=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return ElementoGuardadoCreateSerializer
        return ElementoGuardadoSerializer

    def get_serializer_context(self):
        return {'request': self.request}


# --- Vistas Públicas ---

class PublicacionListView(generics.ListAPIView):
    serializer_class = PublicacionListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['titulo', 'contenido']
    ordering_fields = ['fecha_publicacion', 'titulo']

    def get_queryset(self):
        queryset = Publicacion.objects.filter(es_publicado=True)
        tipos = self.request.query_params.get('tipo', None)
        if tipos:
            lista_tipos = [tipo.strip().upper() for tipo in tipos.split(',')]
            queryset = queryset.filter(tipo__in=lista_tipos)
        return queryset


class PublicacionDetailView(generics.RetrieveAPIView):
    serializer_class = PublicacionDetailSerializer
    permission_classes = [AllowAny]
    queryset = Publicacion.objects.filter(es_publicado=True)
    lookup_field = 'slug'


class ConsejoConsultivoListView(generics.ListAPIView):
    queryset = ConsejoConsultivo.objects.all().order_by('-fecha_publicacion')
    serializer_class = ConsejoConsultivoSerializer
    permission_classes = [AllowAny]


class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all().order_by('-fecha_publicacion')
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]


class CategoriaPrestadorListView(generics.ListAPIView):
    queryset = CategoriaPrestador.objects.all().order_by('nombre')
    serializer_class = CategoriaPrestadorSerializer
    permission_classes = [AllowAny]


class PrestadorServicioPublicListView(generics.ListAPIView):
    serializer_class = PrestadorServicioPublicListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre_negocio', 'descripcion']
    ordering_fields = ['nombre_negocio']

    def get_queryset(self):
        queryset = PrestadorServicio.objects.filter(aprobado=True)
        categoria_slug = self.request.query_params.get('categoria', None)
        if categoria_slug:
            queryset = queryset.filter(categoria__slug=categoria_slug)
        return queryset


class PrestadorServicioPublicDetailView(generics.RetrieveAPIView):
    queryset = PrestadorServicio.objects.filter(aprobado=True)
    serializer_class = PrestadorServicioPublicDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'


class AtractivoTuristicoListView(generics.ListAPIView):
    serializer_class = AtractivoTuristicoListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = AtractivoTuristico.objects.filter(es_publicado=True)
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(categoria_color__iexact=categoria)
        return queryset


class AtractivoTuristicoDetailView(generics.RetrieveAPIView):
    queryset = AtractivoTuristico.objects.filter(es_publicado=True)
    serializer_class = AtractivoTuristicoDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class LocationListView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        locations = []
        prestadores = PrestadorServicio.objects.filter(aprobado=True, ubicacion_mapa__isnull=False).exclude(ubicacion_mapa__exact='')
        for p in prestadores:
            try:
                lat, lng = map(float, p.ubicacion_mapa.split(','))
                locations.append({'id': f'prestador_{p.id}', 'nombre': p.nombre_negocio, 'lat': lat, 'lng': lng, 'tipo': p.categoria.slug if p.categoria else 'prestador', 'url_detalle': None})
            except (ValueError, AttributeError):
                continue
        atractivos = AtractivoTuristico.objects.filter(es_publicado=True, ubicacion_mapa__isnull=False).exclude(ubicacion_mapa__exact='')
        for a in atractivos:
            try:
                lat, lng = map(float, a.ubicacion_mapa.split(','))
                locations.append({'id': f'atractivo_{a.id}', 'nombre': a.nombre, 'lat': lat, 'lng': lng, 'tipo': f'atractivo_{a.categoria_color.lower()}', 'url_detalle': f'/atractivos/{a.slug}'})
            except (ValueError, AttributeError):
                continue
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)


# --- Vistas de Administración ---

class AdminPrestadorListView(generics.ListAPIView):
    queryset = PrestadorServicio.objects.all().order_by('-fecha_creacion')
    serializer_class = AdminPrestadorServicioSerializer
    permission_classes = [IsAdminOrFuncionario]
    filter_backends = [OrderingFilter]
    ordering_fields = ['fecha_creacion', 'nombre_negocio']

    def get_queryset(self):
        queryset = super().get_queryset()
        aprobado_param = self.request.query_params.get('aprobado')
        if aprobado_param is not None:
            aprobado = aprobado_param.lower() == 'true'
            queryset = queryset.filter(aprobado=aprobado)
        return queryset


class AdminApprovePrestadorView(views.APIView):
    permission_classes = [IsAdminOrFuncionario]

    def patch(self, request, pk, *args, **kwargs):
        try:
            prestador = PrestadorServicio.objects.get(pk=pk)
        except PrestadorServicio.DoesNotExist:
            return Response({'error': 'Prestador no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        prestador.aprobado = True
        prestador.save(update_fields=['aprobado'])
        return Response({'status': 'Prestador aprobado con éxito.'}, status=status.HTTP_200_OK)

class ContenidoMunicipioViewSet(viewsets.ModelViewSet):
    queryset = ContenidoMunicipio.objects.all().order_by('orden')
    serializer_class = ContenidoMunicipioSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminOrFuncionario]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


# --- Vista para el Sistema de Agentes ---
class AgentCommandView(views.APIView):
    """
    Endpoint para recibir y procesar comandos para el sistema de agentes jerárquicos.
    """
    permission_classes = [IsAuthenticated]

    @async_to_sync
    async def post(self, request, *args, **kwargs):
        """
        Recibe una orden en lenguaje natural, la valida y la pasa al Coronel de Turismo.
        Usa async_to_sync para puentear el mundo síncrono de Django con el asíncrono de LangGraph.
        """
        from agents.corps.turismo_coronel import get_turismo_coronel_graph

        serializer = AgentCommandSerializer(data=request.data)
        if serializer.is_valid():
            orden = serializer.validated_data['orden']

            coronel_agent = get_turismo_coronel_graph()
            config = {"configurable": {"thread_id": f"user_command_{request.user.id}"}}

            try:
                result = await coronel_agent.ainvoke({
                    "general_order": orden,
                    "app_context": None
                }, config=config)

                final_report = result.get("final_report", "El agente completó la misión pero no generó un informe final.")
                return Response({"respuesta": final_report}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(
                    {"error": f"Error crítico al procesar la orden con el agente: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)