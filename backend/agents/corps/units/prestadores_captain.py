from typing import TypedDict, Any, List
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

class LieutenantTask(BaseModel):
    task_description: str
    responsible_lieutenant: str

class LieutenantPlan(BaseModel):
    plan: List[LieutenantTask]

class PrestadoresCaptainState(TypedDict):
    coronel_order: str
    lieutenant_plan: LieutenantPlan | None
    task_queue: List[LieutenantTask]
    completed_missions: list
    final_report: str
    error: str | None

async def create_lieutenant_plan(state: PrestadoresCaptainState) -> PrestadoresCaptainState:
    print("--- 🧠 CAP. PRESTADORES: Creando Plan de Pelotón (SIMULADO)... ---")
    plan_simulado = LieutenantPlan(plan=[
        LieutenantTask(
            task_description=state['coronel_order'],
            responsible_lieutenant='Prestadores'
        )
    ])
    state.update({"lieutenant_plan": plan_simulado, "task_queue": plan_simulado.plan.copy(), "completed_missions": []})
    return state

def route_to_lieutenant(state: PrestadoresCaptainState):
    if state.get("error") or not state["task_queue"]:
        return "compile_report"

    lieutenant_unit = state["task_queue"][0].responsible_lieutenant
    if lieutenant_unit == 'Prestadores':
        return "prestadores_lieutenant"

    state["error"] = f"Planificación defectuosa: Teniente desconocido '{lieutenant_unit}'."
    state["task_queue"].pop(0)
    return "route_to_lieutenant"

async def prestadores_node(state: PrestadoresCaptainState) -> PrestadoresCaptainState:
    """
    (NODO DE DELEGACIÓN) Carga perezosamente al Teniente y le delega la misión.
    """
    # --- Carga Perezosa del Teniente ---
    from agents.corps.units.platoons.prestadores_teniente import get_prestadores_teniente_graph
    prestadores_lieutenant_agent = get_prestadores_teniente_graph()

    mission = state["task_queue"].pop(0)
    print(f"--- 🔽 CAPITÁN: Delegando a TTE. PRESTADORES -> '{mission.task_description}' ---")
    result = await prestadores_lieutenant_agent.ainvoke({"captain_order": mission.task_description})
    state["completed_missions"].append({"lieutenant": "Prestadores", "report": result.get("final_report", "Sin reporte.")})
    return state

async def compile_final_report(state: PrestadoresCaptainState) -> PrestadoresCaptainState:
    print("--- 📄 CAP. PRESTADORES: Compilando Informe Táctico para el Coronel... ---")
    if state.get("error"):
        state["final_report"] = state["error"]
    else:
        report_body = "\n".join([f"- Reporte del Tte. de {m['lieutenant']}: {m['report']}" for m in state["completed_missions"]])
        state["final_report"] = f"Misión de gestión de Prestadores completada. Resumen:\n{report_body}"
    return state

def get_prestadores_captain_graph():
    workflow = StateGraph(PrestadoresCaptainState)
    workflow.add_node("planner", create_lieutenant_plan)
    workflow.add_node("router", lambda s: s)
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