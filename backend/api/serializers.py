from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUser, PrestadorServicio, ImagenGaleria, DocumentoLegalizacion, Publicacion, ConsejoConsultivo

class ConsejoConsultivoSerializer(serializers.ModelSerializer):
    """
    Serializador para las publicaciones del Consejo Consultivo.
    """
    class Meta:
        model = ConsejoConsultivo
        fields = ['id', 'titulo', 'contenido', 'fecha_publicacion', 'documento_adjunto']

class PublicacionListSerializer(serializers.ModelSerializer):
    """
    Serializador para listar las publicaciones para el público.
    Muestra una versión resumida de la información.
    """
    class Meta:
        model = Publicacion
        fields = ['id', 'tipo', 'titulo', 'slug', 'imagen_principal', 'fecha_evento_inicio', 'fecha_evento_fin', 'fecha_publicacion']

class PublicacionDetailSerializer(serializers.ModelSerializer):
    """
    Serializador para ver el detalle completo de una publicación.
    """
    autor_nombre = serializers.CharField(source='autor.get_full_name', read_only=True)

    class Meta:
        model = Publicacion
        fields = [
            'id', 'tipo', 'titulo', 'slug', 'contenido', 'imagen_principal',
            'autor_nombre', 'fecha_evento_inicio', 'fecha_evento_fin', 'fecha_publicacion'
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


class CustomRegisterSerializer(RegisterSerializer):
    """
    Serializador de registro personalizado.
    Cuando un usuario se registra, automáticamente se le asigna el rol 'PRESTADOR'
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