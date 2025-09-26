from typing import TypedDict, Any, List
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from backend.agents.corps.units.platoons.prestadores_teniente import get_prestadores_teniente_graph

# --- DEFINICIÓN DEL ESTADO Y PLAN DEL CAPITÁN ---

class LieutenantTask(BaseModel):
    """Define una misión específica para ser asignada a un pelotón de Tenientes."""
    task_description: str = Field(description="La descripción detallada de la misión para el Teniente.")
    responsible_lieutenant: str = Field(description="El Teniente especialista. Por ahora, solo 'Prestadores'.")

class LieutenantPlan(BaseModel):
    """El plan de pelotón generado por el Capitán."""
    plan: List[LieutenantTask] = Field(description="La lista de misiones para los Tenientes.")

class PrestadoresCaptainState(TypedDict):
    """La pizarra táctica del Capitán de Prestadores."""
    coronel_order: str
    lieutenant_plan: LieutenantPlan | None
    task_queue: List[LieutenantTask]
    completed_missions: list
    final_report: str
    error: str | None

# --- PUESTO DE MANDO: INSTANCIACIÓN DE TENIENTES ---
prestadores_lieutenant_agent = get_prestadores_teniente_graph()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# --- NODOS DEL GRAFO DE MANDO DEL CAPITÁN ---

async def create_lieutenant_plan(state: PrestadoresCaptainState) -> PrestadoresCaptainState:
    """(NODO 1: PLANIFICADOR SIMULADO) Devuelve un plan predefinido para el Teniente."""
    print("--- 🧠 CAP. PRESTADORES: Creando Plan de Pelotón (SIMULADO)... ---")

    # Simulamos el plan que el LLM debería generar.
    plan_simulado = LieutenantPlan(plan=[
        LieutenantTask(
            task_description=state['coronel_order'], # Pasamos la orden completa al Teniente
            responsible_lieutenant='Prestadores'
        )
    ])

    print(f"--- 📝 CAP. PRESTADORES: Plan de Pelotón Generado. Pasos: {len(plan_simulado.plan)} ---")
    state.update({"lieutenant_plan": plan_simulado, "task_queue": plan_simulado.plan.copy(), "completed_missions": []})
    return state

def route_to_lieutenant(state: PrestadoresCaptainState):
    """(NODO 2: ENRUTADOR) Lee la siguiente misión y dirige el flujo al Teniente correcto."""
    if state.get("error") or not state["task_queue"]:
        return "compile_report"

    lieutenant_unit = state["task_queue"][0].responsible_lieutenant
    if lieutenant_unit == 'Prestadores':
        return "prestadores_lieutenant"

    state["error"] = f"Planificación defectuosa: Teniente desconocido '{lieutenant_unit}'."
    state["task_queue"].pop(0)
    return "route_to_lieutenant"

async def prestadores_node(state: PrestadoresCaptainState) -> PrestadoresCaptainState:
    """Invoca al sub-grafo del Teniente de Prestadores."""
    mission = state["task_queue"].pop(0)
    print(f"--- 🔽 CAPITÁN: Delegando a TTE. PRESTADORES -> '{mission.task_description}' ---")
    result = await prestadores_lieutenant_agent.ainvoke({"captain_order": mission.task_description})
    state["completed_missions"].append({"lieutenant": "Prestadores", "report": result.get("final_report", "Sin reporte.")})
    return state

async def compile_final_report(state: PrestadoresCaptainState) -> PrestadoresCaptainState:
    """(NODO FINAL: INFORME TÁCTICO) Sintetiza los reportes de los Tenientes para el Coronel."""
    print("--- 📄 CAP. PRESTADORES: Compilando Informe Táctico para el Coronel... ---")
    if state.get("error"):
        state["final_report"] = state["error"]
    else:
        report_body = "\n".join([f"- Reporte del Tte. de {m['lieutenant']}: {m['report']}" for m in state["completed_missions"]])
        state["final_report"] = f"Misión de gestión de Prestadores completada. Resumen:\n{report_body}"
    return state

# --- ENSAMBLAJE DEL GRAFO DE MANDO DEL CAPITÁN ---

def get_prestadores_captain_graph():
    workflow = StateGraph(PrestadoresCaptainState)
    workflow.add_node("planner", create_lieutenant_plan)
    workflow.add_node("router", lambda s: s) # Nodo 'passthrough'
    workflow.add_node("prestadores_lieutenant", prestadores_node)
    workflow.add_node("compiler", compile_final_report)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "router")

    workflow.add_conditional_edges(
        "router",
        route_to_lieutenant,
        {
            "prestadores_lieutenant": "prestadores_lieutenant",
            "compile_report": "compiler",
            "route_to_lieutenant": "router"
        }
    )

    workflow.add_edge("prestadores_lieutenant", "router")
    workflow.add_edge("compiler", END)

    return workflow.compile()