import asyncio
from backend.agents.corps.turismo_coronel import get_turismo_coronel_graph

async def main():
    """
    Script para probar el sistema de agentes de IA de forma aislada.
    Invoca al Coronel de Turismo con una orden de prueba y muestra el resultado.
    """
    print("--- INICIANDO PRUEBA DEL SISTEMA DE AGENTES ---")

    # 1. Obtenemos el grafo del agente Coronel
    # La función `get_turismo_coronel_graph` ya no está, se debe usar la que está dentro de `turismo_coronel.py`
    # El problema es que el coronel está esperando un LLM, y no lo tenemos disponible
    # Vamos a usar el plan simulado que ya existe en el código del coronel

    # La orden que vamos a simular
    orden_de_prueba = "Crear un nuevo perfil de prestador de servicios para el restaurante 'La Brasa Llanera', con email 'brasa@example.com', slug de categoría 'restaurantes' y teléfono '3123456789'."

    print(f"\n[ORDEN DE PRUEBA]: {orden_de_prueba}\n")

    # 2. Obtenemos el grafo del agente Coronel
    # No es necesario compilarlo, ya que la función get lo devuelve compilado
    coronel_agent = get_turismo_coronel_graph()

    # 3. Configuramos el hilo de la conversación (necesario para LangGraph)
    config = {"configurable": {"thread_id": "test-thread-1"}}

    # 4. Invocamos al agente con la orden
    try:
        # El agente Coronel espera un diccionario con "general_order"
        result = await coronel_agent.ainvoke({
            "general_order": orden_de_prueba,
            "app_context": None # No pasamos contexto por ahora
        }, config=config)

        # 5. Imprimimos el informe final
        final_report = result.get("final_report", "El agente no generó un informe final.")
        print("\n--- INFORME FINAL DEL CORONEL ---")
        print(final_report)
        print("---------------------------------\n")

    except Exception as e:
        print(f"\n--- ❌ ERROR CRÍTICO DURANTE LA PRUEBA DEL AGENTE ---")
        print(f"Error: {e}")
        print("-----------------------------------------------------\n")

if __name__ == "__main__":
    # Necesitamos ejecutar esto en un contexto donde Django esté inicializado
    # para que el ORM funcione en las herramientas.
    # Este script debe ser ejecutado con `python manage.py shell < test_agent.py`

    # Para poder ejecutarlo directamente, necesitamos configurar Django
    import os
    import django

    # Esto es un poco hacky, pero necesario para un script independiente
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.puerto_gaitan_turismo.settings')
    django.setup()

    # Ahora que Django está configurado, podemos ejecutar el main asíncrono
    asyncio.run(main())