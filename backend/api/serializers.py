from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import (
    CustomUser, PrestadorServicio, ImagenGaleria, DocumentoLegalizacion, Publicacion,
    ConsejoConsultivo, AtractivoTuristico, ImagenAtractivo, ElementoGuardado, ContentType,
    CategoriaPrestador, Video, ContenidoMunicipio
)

class VideoSerializer(serializers.ModelSerializer):
    """
    Serializador para los videos.
    """
    class Meta:
        model = Video
        fields = ['id', 'titulo', 'descripcion', 'url_youtube', 'fecha_publicacion']


class ConsejoConsultivoSerializer(serializers.ModelSerializer):
    """
    Serializador para las publicaciones del Consejo Consultivo.
    """
    class Meta:
        model = ConsejoConsultivo
        fields = ['id', 'titulo', 'contenido', 'fecha_publicacion', 'documento_adjunto']


class LocationSerializer(serializers.Serializer):
    """
    Serializador genérico para representar cualquier punto geolocalizado en el mapa.
    No está atado a un modelo, lo que permite combinar diferentes tipos de ubicaciones.
    """
    id = serializers.CharField()
    nombre = serializers.CharField()
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    tipo = serializers.CharField()
    url_detalle = serializers.CharField()


class ImagenAtractivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenAtractivo
        fields = ['id', 'imagen', 'alt_text']


class AtractivoTuristicoListSerializer(serializers.ModelSerializer):
    """
    Serializador para la lista pública de atractivos turísticos.
    """
    imagen_principal = serializers.SerializerMethodField()

    class Meta:
        model = AtractivoTuristico
        fields = ['id', 'nombre', 'slug', 'categoria_color', 'imagen_principal']

    def get_imagen_principal(self, obj):
        # Devuelve la URL de la primera imagen de la galería, o None si no hay.
        primera_imagen = obj.imagenes.first()
        if primera_imagen:
            request = self.context.get('request')
            return request.build_absolute_uri(primera_imagen.imagen.url)
        return None


class AtractivoTuristicoDetailSerializer(serializers.ModelSerializer):
    """
    Serializador para el detalle público de un atractivo turístico.
    """
    imagenes = ImagenAtractivoSerializer(many=True, read_only=True)
    categoria_color_display = serializers.CharField(source='get_categoria_color_display', read_only=True)

    class Meta:
        model = AtractivoTuristico
        fields = [
            'id', 'nombre', 'slug', 'descripcion', 'como_llegar',
            'ubicacion_mapa', 'categoria_color', 'categoria_color_display', 'imagenes'
        ]


class PublicacionListSerializer(serializers.ModelSerializer):
    """
    Serializador para listar las publicaciones para el público.
    Muestra una versión resumida de la información.
    """
    class Meta:
        model = Publicacion
        fields = ['id', 'tipo', 'subcategoria_evento', 'titulo', 'slug', 'imagen_principal', 'fecha_evento_inicio', 'fecha_evento_fin', 'fecha_publicacion']

class PublicacionDetailSerializer(serializers.ModelSerializer):
    """
    Serializador para ver el detalle completo de una publicación.
    """
    autor_nombre = serializers.CharField(source='autor.get_full_name', read_only=True)
    subcategoria_evento_display = serializers.CharField(source='get_subcategoria_evento_display', read_only=True)

    class Meta:
        model = Publicacion
        fields = [
            'id', 'tipo', 'titulo', 'slug', 'contenido', 'imagen_principal',
            'autor_nombre', 'fecha_evento_inicio', 'fecha_evento_fin', 'fecha_publicacion',
            'subcategoria_evento', 'subcategoria_evento_display'
        ]

class ImagenGaleriaSerializer(serializers.ModelSerializer):
    """
    Serializador para subir y listar imágenes de la galería de un prestador.
    """
    class Meta:
        model = ImagenGaleria
        fields = ['id', 'imagen', 'alt_text', 'prestador']
        read_only_fields = ['prestador']

class DocumentoLegalizacionSerializer(serializers.ModelSerializer):
    """
    Serializador para subir y listar documentos de legalización de un prestador.
    """
    class Meta:
        model = DocumentoLegalizacion
        fields = ['id', 'documento', 'nombre_documento', 'fecha_subida', 'prestador']
        read_only_fields = ['prestador', 'fecha_subida']


class CategoriaPrestadorSerializer(serializers.ModelSerializer):
    """
    Serializador para las categorías de los prestadores de servicios.
    """
    class Meta:
        model = CategoriaPrestador
        fields = ['id', 'nombre', 'slug']


class PrestadorServicioPublicListSerializer(serializers.ModelSerializer):
    """
    Serializador para la vista pública de la lista de prestadores de servicios.
    """
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    imagen_principal = serializers.SerializerMethodField()

    class Meta:
        model = PrestadorServicio
        fields = ['id', 'nombre_negocio', 'categoria_nombre', 'imagen_principal']

    def get_imagen_principal(self, obj):
        primera_imagen = obj.galeria_imagenes.first()
        if primera_imagen:
            request = self.context.get('request')
            return request.build_absolute_uri(primera_imagen.imagen.url)
        return None


class PrestadorServicioPublicDetailSerializer(serializers.ModelSerializer):
    """
    Serializador para el detalle público de un prestador de servicios.
    """
    categoria = CategoriaPrestadorSerializer(read_only=True)
    galeria_imagenes = ImagenGaleriaSerializer(many=True, read_only=True)

    class Meta:
        model = PrestadorServicio
        # Excluimos campos sensibles o de gestión interna
        exclude = ['usuario', 'aprobado', 'reporte_ocupacion_nacional', 'reporte_ocupacion_internacional']


class PrestadorServicioSerializer(serializers.ModelSerializer):
    """
    Serializador para que un prestador vea y actualice su perfil.
    """
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    galeria_imagenes = ImagenGaleriaSerializer(many=True, read_only=True)
    documentos_legalizacion = DocumentoLegalizacionSerializer(many=True, read_only=True)

    class Meta:
        model = PrestadorServicio
        fields = [
            'nombre_negocio', 'descripcion', 'telefono', 'email_contacto',
            'red_social_facebook', 'red_social_instagram', 'red_social_whatsapp',
            'ubicacion_mapa', 'promociones_ofertas',
            'reporte_ocupacion_nacional', 'reporte_ocupacion_internacional',
            'categoria_nombre', 'aprobado',
            'galeria_imagenes', 'documentos_legalizacion'
        ]
        read_only_fields = ['aprobado', 'categoria_nombre', 'galeria_imagenes', 'documentos_legalizacion']


class TuristaRegisterSerializer(RegisterSerializer):
    """
    Serializador de registro simplificado para usuarios turistas.
    Cuando un usuario se registra, automáticamente se le asigna el rol 'TURISTA'.
    """
    def save(self, request):
        user = super().save(request)
        user.role = CustomUser.Role.TURISTA
        user.save()
        return user


class PrestadorRegisterSerializer(RegisterSerializer):
    """
    Serializador de registro para Prestadores de Servicios.
    Cuando un usuario se registra por esta vía, se le asigna el rol 'PRESTADOR'
    y se le crea un perfil de PrestadorServicio vacío.
    """

    def save(self, request):
        # El método save original crea el usuario. Lo llamamos primero.
        user = super().save(request)

        # Asignamos el rol de PRESTADOR
        user.role = CustomUser.Role.PRESTADOR
        user.save()

        # Creamos el perfil de Prestador de Servicio asociado
        # Usamos el username como nombre de negocio temporal
        PrestadorServicio.objects.create(
            usuario=user,
            nombre_negocio=f"Perfil de {user.username}"
        )

        return user


class ElementoGuardadoSerializer(serializers.ModelSerializer):
    """
    Serializador para mostrar los elementos guardados por un usuario.
    Determina dinámicamente qué serializador usar para el objeto guardado.
    """
    content_object = serializers.SerializerMethodField()
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)

    class Meta:
        model = ElementoGuardado
        fields = ['id', 'fecha_guardado', 'object_id', 'content_type_name', 'content_object']

    def get_content_object(self, obj):
        if isinstance(obj.content_object, AtractivoTuristico):
            return AtractivoTuristicoListSerializer(obj.content_object, context=self.context).data
        if isinstance(obj.content_object, Publicacion):
            return PublicacionListSerializer(obj.content_object, context=self.context).data
        return None

class ElementoGuardadoCreateSerializer(serializers.ModelSerializer):
    """
    Serializador para que un usuario guarde un nuevo elemento favorito.
    """
    content_type = serializers.CharField()

    class Meta:
        model = ElementoGuardado
        fields = ['content_type', 'object_id']

    def validate(self, data):
        content_type_str = data['content_type'].lower()
        model_map = {
            'atractivoturistico': AtractivoTuristico,
            'publicacion': Publicacion,
        }
        model = model_map.get(content_type_str)

        if not model:
            raise serializers.ValidationError("Tipo de contenido no válido.")

        if not model.objects.filter(pk=data['object_id']).exists():
            raise serializers.ValidationError("El objeto especificado no existe.")

        data['content_type'] = ContentType.objects.get_for_model(model)
        return data

    def create(self, validated_data):
        # get_or_create para manejar la creación de forma idempotente.
        # Si ya existe, simplemente lo devuelve.
        instance, _ = ElementoGuardado.objects.get_or_create(
            usuario=self.context['request'].user,
            content_type=validated_data['content_type'],
            object_id=validated_data['object_id']
        )
        return instance


class AdminPrestadorServicioSerializer(serializers.ModelSerializer):
    """
    Serializador para que el administrador vea la lista de prestadores.
    Incluye todos los campos relevantes para la moderación.
    """
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)

    class Meta:
        model = PrestadorServicio
        fields = [
            'id',
            'nombre_negocio',
            'telefono',
            'email_contacto',
            'aprobado',
            'fecha_creacion',
            'categoria_nombre',
            'usuario_email'
        ]
 


class ContenidoMunicipioSerializer(serializers.ModelSerializer):
    """
    Serializador para los bloques de contenido del municipio.
    """
    actualizado_por_username = serializers.CharField(source='actualizado_por.username', read_only=True)

    class Meta:
        model = ContenidoMunicipio
        fields = [
            'id',
            'seccion',
            'titulo',
            'contenido',
            'orden',
            'actualizado_por_username',
            'fecha_actualizacion',
        ]

    def create(self, validated_data):
        # Asigna el usuario actual al crear un nuevo bloque
        validated_data['actualizado_por'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Asigna el usuario actual al actualizar un bloque
        validated_data['actualizado_por'] = self.context['request'].user
        return super().update(instance, validated_data)


# --- Serializador para el Agente ---

class AgentCommandSerializer(serializers.Serializer):
    """
    Serializador para validar la orden enviada al sistema de agentes.
    """
    orden = serializers.CharField(
        max_length=2000,
        help_text="La orden o instrucción en lenguaje natural para el agente Coronel."
    )