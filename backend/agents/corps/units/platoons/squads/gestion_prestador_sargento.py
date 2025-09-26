from .sargento_base_graph import SargentoGraphBuilder
from backend.tools.herramientas_prestador import PrestadorSoldiers
from typing import Any

def get_gestion_prestador_sargento_builder():
    """
    Returns a function (a builder) that can construct the sargento agent
    once provided with the necessary context, like an api_client.
    This follows a factory or builder pattern.
    """
    def build_sargento_agent(api_client: Any):
        """Builds the sargento's compiled graph using the provided api_client."""

        # El Sargento recluta a su escuadra de soldados especialistas
        squad = PrestadorSoldiers(api_client).get_all_soldiers()

        # Construye el grafo de mando usando la plantilla estandarizada
        builder = SargentoGraphBuilder(squad, squad_name="Gestión de Prestadores")
        return builder.build_graph()

    print("✅ Doctrina aplicada: Sargento de Gestión de Prestadores listo para el despliegue.")

    # Devuelve la función constructora, no el agente compilado.
    return build_sargento_agent