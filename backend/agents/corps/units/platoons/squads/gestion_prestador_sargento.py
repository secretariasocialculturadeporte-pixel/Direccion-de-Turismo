from .sargento_base_graph import SargentoGraphBuilder
from backend.tools.herramientas_prestador import PrestadorSoldiers
from typing import Any


def get_gestion_prestador_sargento_builder():
    """
    Devuelve una función (builder) que puede construir el agente sargento
    cuando se le proporcione el contexto necesario, como un api_client.
    Sigue el patrón factory/builder.
    """

    def build_sargento_agent(api_client: Any):
        """Construye el grafo del Sargento usando el api_client proporcionado."""

        # El Sargento recluta a su escuadra de soldados especialistas
        squad = PrestadorSoldiers(api_client).get_all_soldiers()

        # Construye el grafo de mando usando la plantilla estandarizada
        builder = SargentoGraphBuilder(squad, squad_name="Gestión de Prestadores")
        return builder.build_graph()

    print("✅ Doctrina aplicada: Sargento de Gestión de Prestadores listo para el despliegue.")

    # Devuelve la función constructora, no el agente compilado.
    return build_sargento_agent