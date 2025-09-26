from typing import TypedDict, Any, List
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field
from importlib import import_module
from langchain_openai import ChatOpenAI

# --- Modelos de Planificación del Capitán ---
class LieutenantTask(BaseModel):
    """Define una misión específica para ser asignada a un Teniente especialista."""
    task_description: str = Field(description="La descripción detallada de la misión para el Teniente.")
    responsible_lieutenant: str = Field(description="El Teniente especialista. Debe ser uno de: 'Hoteles', 'Restaurantes', 'Guias', 'Agencias', 'Transporte'.")

class LieutenantPlan(BaseModel):
    """El plan de pelotón generado por el Capitán."""
    plan: List[LieutenantTask]

# --- Estado del Grafo del Capitán ---
class PrestadoresCaptainState(TypedDict):
    coronel_order: str
    lieutenant_plan: LieutenantPlan | None
    task_queue: List[LieutenantTask]
    completed_missions: list
    final_report: str
    error: str | None

# --- NODO 1: PLANIFICADOR TÁCTICO REAL ---
async def create_lieutenant_plan(state: PrestadoresCaptainState) -> PrestadoresCaptainState:
    """
    (CEREBRO REAL) Analiza la orden del Coronel y la descompone en un plan de acción,
    delegando la tarea al Teniente especialista apropiado usando un LLM.
    """
    print("--- 🧠 CAP. PRESTADORES: Creando Plan de Pelotón Táctico... ---")

    prompt = f"""
Eres un Capitán de Prestadores de Servicios Turísticos. Tu Coronel te ha dado una orden.
Tu deber es analizarla y crear un plan de un solo paso, asignando la misión al Teniente especialista correcto.

Tenientes bajo tu mando y sus especialidades:
- 'Hoteles': Se encarga de todo lo relacionado con alojamiento (hoteles, cabañas, hostales).
- 'Restaurantes': Se encarga de todo lo relacionado con gastronomía (restaurantes, bares).
- 'Guias': Se encarga de guías turísticos y baquianos.
- 'Agencias': Se encarga de agencias de viajes.
- 'Transporte': Se encarga de transporte turístico.

Orden del Coronel: "{state['coronel_order']}"

Genera el plan en formato JSON.
"""
    try:
        structured_llm = ChatOpenAI(model="gpt-4o", temperature=0).with_structured_output(LieutenantPlan)
        plan = await structured_llm.ainvoke(prompt)
        state.update({"lieutenant_plan": plan, "task_queue": plan.plan.copy(), "completed_missions": []})
    except Exception as e:
        state["error"] = f"Error del LLM al planificar para el Capitán de Prestadores: {e}"
    return state

# --- NODO 2: ENRUTADOR DE PELOTÓN ---
def route_to_lieutenant(state: PrestadoresCaptainState):
    if state.get("error") or not state["task_queue"]:
        return "compile_report"
    return f"{state['task_queue'][0].responsible_lieutenant.lower()}_lieutenant"

# --- NODO 3: DELEGACIÓN GENÉRICA A TENIENTES ---
async def generic_lieutenant_node(state: PrestadoresCaptainState, teniente_module_name: str, teniente_graph_func_name: str, teniente_name: str) -> PrestadoresCaptainState:
    mission = state["task_queue"].pop(0)
    print(f"--- 🚀 CAPITÁN: Delegando a TTE. {teniente_name.upper()} -> '{mission.task_description}' ---")
    try:
        module = import_module(f"agents.corps.units.platoons.{teniente_module_name}")
        get_teniente_graph = getattr(module, teniente_graph_func_name)
        lieutenant_agent = get_teniente_graph()

        result = await lieutenant_agent.ainvoke({"captain_order": mission.task_description, "app_context": state.get("app_context")})
        state["completed_missions"].append({"lieutenant": teniente_name, "report": result.get("final_report", "Sin reporte.")})
    except Exception as e:
        state["error"] = f"Error durante la delegación al Teniente {teniente_name}: {e}"
    return state

# --- NODO FINAL: COMPILADOR DE INFORMES ---
async def compile_final_report(state: PrestadoresCaptainState) -> PrestadoresCaptainState:
    if state.get("error"):
        state["final_report"] = state["error"]
    else:
        report_body = "\n".join([f"- Reporte del Tte. de {m['lieutenant']}: {m['report']}" for m in state["completed_missions"]])
        state["final_report"] = f"Misión de gestión de Prestadores completada. Resumen:\n{report_body}"
    return state

# --- ENSAMBLAJE DEL GRAFO ---
def get_prestadores_captain_graph():
    workflow = StateGraph(PrestadoresCaptainState)
    workflow.add_node("planner", create_lieutenant_plan)
    workflow.add_node("router", lambda s: s)

    lieutenant_nodes = {
        "hoteles_lieutenant": ("hoteles_teniente", "get_hoteles_teniente_graph", "Hoteles"),
        "restaurantes_lieutenant": ("restaurantes_teniente", "get_restaurantes_teniente_graph", "Restaurantes"),
        "guias_lieutenant": ("guias_teniente", "get_guias_teniente_graph", "Guias"),
        "agencias_lieutenant": ("agencias_teniente", "get_agencias_teniente_graph", "Agencias"),
        "transporte_lieutenant": ("transporte_teniente", "get_transporte_teniente_graph", "Transporte"),
    }
    for node_name, (module, func, display) in lieutenant_nodes.items():
        workflow.add_node(node_name, lambda s, m=module, f=func, d=display: generic_lieutenant_node(s, m, f, d))

    workflow.add_node("compiler", compile_final_report)
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "router")

    conditional_map = {name: name for name in lieutenant_nodes.keys()}
    conditional_map["compile_report"] = "compiler"
    workflow.add_conditional_edges("router", route_to_lieutenant, conditional_map)

    for node_name in lieutenant_nodes.keys():
        workflow.add_edge(node_name, "router")

    workflow.add_edge("compiler", END)
    return workflow.compile()