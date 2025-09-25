import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

def prestador_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/prestadores/<username>/<filename>
    return f'prestadores/{instance.usuario.username}/{filename}'

def galeria_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/prestadores/<username>/galeria/<filename>
    return f'prestadores/{instance.prestador.usuario.username}/galeria/{filename}'

def documentos_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/prestadores/<username>/documentos/<filename>
    return f'prestadores/{instance.prestador.usuario.username}/documentos/{filename}'


class CustomUser(AbstractUser):
    """
    Modelo de Usuario personalizado que extiende el de Django.
    Añade un campo 'rol' para diferenciar los tipos de usuario.
    """
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Administrador General")
        FUNCIONARIO = "FUNCIONARIO", _("Funcionario de Turismo")
        PRESTADOR = "PRESTADOR", _("Prestador de Servicio")

    base_role = Role.ADMIN

    role = models.CharField(_("Rol"), max_length=50, choices=Role.choices, default=base_role)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)


class CategoriaPrestador(models.Model):
    """
    Categorías para los prestadores de servicios (Hotel, Restaurante, Artesano, etc.)
    """
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, help_text="Versión del nombre amigable para URLs")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría de Prestador"
        verbose_name_plural = "Categorías de Prestadores"


class PrestadorServicio(models.Model):
    """
    Modelo central para cada prestador de servicio turístico.
    """
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="perfil_prestador")
    categoria = models.ForeignKey(CategoriaPrestador, on_delete=models.SET_NULL, null=True, related_name="prestadores")
    nombre_negocio = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email_contacto = models.EmailField(max_length=254, blank=True, null=True)
    red_social_facebook = models.URLField(blank=True, null=True)
    red_social_instagram = models.URLField(blank=True, null=True)
    red_social_whatsapp = models.CharField(max_length=20, blank=True, null=True, help_text="Número de WhatsApp con código de país")
    ubicacion_mapa = models.CharField(max_length=255, blank=True, null=True, help_text="Coordenadas (lat,lng) o dirección")
    promociones_ofertas = models.TextField(blank=True, null=True, help_text="Detalles de promociones, menús, paquetes, etc.")

    # Campo de moderación
    aprobado = models.BooleanField(default=False, help_text="El administrador debe aprobar este perfil para que sea visible.")

    # Reporte de ocupación para hoteles
    reporte_ocupacion_nacional = models.PositiveIntegerField(default=0, help_text="Exclusivo para hoteles")
    reporte_ocupacion_internacional = models.PositiveIntegerField(default=0, help_text="Exclusivo para hoteles")

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_negocio

    class Meta:
        verbose_name = "Prestador de Servicio"
        verbose_name_plural = "Prestadores de Servicios"


class ImagenGaleria(models.Model):
    prestador = models.ForeignKey(PrestadorServicio, on_delete=models.CASCADE, related_name="galeria_imagenes")
    imagen = models.ImageField(upload_to=galeria_directory_path)
    alt_text = models.CharField(max_length=255, blank=True, help_text="Texto alternativo para accesibilidad")

    def __str__(self):
        return f"Imagen de {self.prestador.nombre_negocio}"


class DocumentoLegalizacion(models.Model):
    prestador = models.ForeignKey(PrestadorServicio, on_delete=models.CASCADE, related_name="documentos_legalizacion")
    documento = models.FileField(upload_to=documentos_directory_path)
    nombre_documento = models.CharField(max_length=100)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_documento} de {self.prestador.nombre_negocio}"


class Publicacion(models.Model):
    """
    Modelo para Eventos, Noticias, Blog y Capacitaciones.
    """
    class Tipo(models.TextChoices):
        EVENTO = "EVENTO", _("Evento")
        NOTICIA = "NOTICIA", _("Noticia")
        BLOG = "BLOG", _("Blog")
        CAPACITACION = "CAPACITACION", _("Capacitación")

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    contenido = models.TextField()
    imagen_principal = models.ImageField(upload_to='publicaciones/', blank=True, null=True)
    autor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="publicaciones")

    # Campos específicos para eventos
    fecha_evento_inicio = models.DateTimeField(blank=True, null=True)
    fecha_evento_fin = models.DateTimeField(blank=True, null=True)

    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    es_publicado = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.titulo}"

    class Meta:
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"
        ordering = ['-fecha_publicacion']


class Video(models.Model):
    """
    Modelo para la sección de videos.
    """
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    url_youtube = models.URLField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class ConsejoConsultivo(models.Model):
    """
    Modelo para la información del Consejo Consultivo de Turismo.
    Permite al administrador publicar actas, noticias o información relevante.
    """
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_publicacion = models.DateField()
    documento_adjunto = models.FileField(
        upload_to='consejo_consultivo/',
        blank=True,
        null=True,
        help_text="Documento opcional (PDF, Word, etc.)"
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Publicación del Consejo Consultivo"
        verbose_name_plural = "Publicaciones del Consejo Consultivo"
        ordering = ['-fecha_publicacion']