from langchain_core.tools import tool
from typing import Any, List, Dict

class PrestadorSoldiers:
    """
    El arsenal de herramientas de ejecución (la escuadra de Soldados)
    para las operaciones de Prestadores de Servicios Turísticos.
    Son comandados por un Sargento especialista en gestión de prestadores.
    """
    def __init__(self, api_client: Any):
        # En una aplicación real, este sería el cliente de la API
        # que interactúa con los modelos de PrestadorServicio, CustomUser, etc.
        self.api = api_client

    @tool
    def crear_perfil_prestador(self, email: str, nombre_negocio: str, categoria_slug: str, telefono: str) -> Dict:
        """
        (SOLDADO DE REGISTRO) Ejecuta la creación de un nuevo usuario de tipo PRESTADOR
        y su perfil de servicio asociado. Requiere un email único, el nombre del negocio,
        el slug de la categoría (ej. 'hoteles', 'restaurantes') y un teléfono.
        Devuelve el ID del nuevo prestador.
        """
        print(f"--- 💥 SOLDADO (Registro): ¡ACCIÓN! Creando perfil para '{nombre_negocio}' con email {email}. ---")
        # Lógica simulada de API:
        # user = self.api.create_user(email=email, role='PRESTADOR')
        # prestador = self.api.create_prestador_profile(user_id=user['id'], ...)
        return {"status": "success", "prestador_id": 123, "message": f"Usuario y perfil para '{nombre_negocio}' creados. El perfil está pendiente de aprobación."}

    @tool
    def actualizar_datos_negocio(self, prestador_id: int, descripcion: str = None, facebook_url: str = None, instagram_url: str = None) -> Dict:
        """
        (SOLDADO DE ACTUALIZACIÓN) Ejecuta la actualización de los datos de un perfil
        de prestador de servicios ya existente.
        """
        print(f"--- 💥 SOLDADO (Actualización): ¡ACCIÓN! Actualizando datos para el prestador_id {prestador_id}. ---")
        # Lógica simulada de API:
        # self.api.update_prestador(prestador_id, descripcion=descripcion, ...)
        return {"status": "success", "prestador_id": prestador_id, "message": "Datos del negocio actualizados correctamente."}

    @tool
    def agregar_foto_galeria(self, prestador_id: int, url_imagen: str, alt_text: str) -> Dict:
        """
        (SOLDADO DE GALERÍA) Sube una nueva imagen a la galería de un prestador de servicios.
        Requiere el ID del prestador, la URL de la imagen y un texto alternativo.
        """
        print(f"--- 💥 SOLDADO (Galería): ¡ACCIÓN! Agregando imagen a la galería del prestador_id {prestador_id}. ---")
        # Lógica simulada de API:
        # image = self.api.upload_gallery_image(prestador_id, url_imagen, alt_text)
        return {"status": "success", "image_id": 987, "message": "Imagen añadida a la galería con éxito."}

    def get_all_soldiers(self) -> List:
        """ Recluta y devuelve la Escuadra de Prestadores completa. """
        return [
            self.crear_perfil_prestador,
            self.actualizar_datos_negocio,
            self.agregar_foto_galeria,
        ]