from typing import TypedDict, List
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END

# No se importa nada de agentes aquí para evitar la carga inicial

class CaptainTask(BaseModel):
    task_description: str
    responsible_captain: str

class TacticalPlan(BaseModel):
    plan: List[CaptainTask]

class TurismoColonelState(TypedDict):
    general_order: str
    tactical_plan: TacticalPlan | None
    task_queue: List[CaptainTask]
    completed_missions: list
    final_report: str
    error: str | None

async def create_tactical_plan(state: TurismoColonelState) -> TurismoColonelState:
    """
    (NODO 1: PLANIFICADOR TÁCTICO SIMULADO)
    Genera un plan predefinido para la prueba.
    """
    print("--- 🧠 CORONEL DE TURISMO: Creando Plan Táctico (SIMULADO)... ---")
    plan_simulado = TacticalPlan(plan=[
        CaptainTask(
            task_description=state['general_order'],
            responsible_captain='Prestadores'
        )
    ])
    state.update({
        "tactical_plan": plan_simulado,
        "task_queue": plan_simulado.plan.copy(),
        "completed_missions": [],
        "error": None
    })
    return state

def route_to_captain(state: TurismoColonelState):
    if state.get("error") or not state["task_queue"]:
        return "compile_report"

    captain_unit = state["task_queue"][0].responsible_captain
    print(f"--- 🧭 CORONEL DE TURISMO: Enrutando misión a Capitán '{captain_unit}' ---")
    if captain_unit == 'Prestadores':
        return "prestadores_captain"
    else:
        state["error"] = f"Planificación defectuosa: Capitán desconocido '{captain_unit}'."
        state["task_queue"].pop(0)
        return "route_to_captain"

async def prestadores_captain_node(state: TurismoColonelState) -> TurismoColonelState:
    """
    (NODO DE DELEGACIÓN) Carga perezosamente al Capitán y le delega la misión.
    """
    # --- Carga Perezosa del Capitán ---
    from agents.corps.units.prestadores_captain import get_prestadores_captain_graph
    prestadores_captain_agent = get_prestadores_captain_graph()

    mission = state["task_queue"].pop(0)
    print(f"--- 🔽 CORONEL: Delegando a CAP. PRESTADORES -> '{mission.task_description}' ---")
    result = await prestadores_captain_agent.ainvoke({"coronel_order": mission.task_description})
    state["completed_missions"].append({
        "captain": "Prestadores",
        "mission": mission.task_description,
        "report": result.get("final_report", "Sin reporte.")
    })
    return state

async def compile_final_report(state: TurismoColonelState) -> TurismoColonelState:
    print("--- 📄 CORONEL DE TURISMO: Compilando Informe de División para el General... ---")
    if state.get("error"):
        state["final_report"] = f"Misión de la División fallida. Razón: {state['error']}"
    else:
        report_body = "\n".join(
            [f"- Reporte del Capitán de {m['captain']}:\n  Misión: '{m['mission']}'\n  Resultado: {m['report']}"
             for m in state["completed_missions"]]
        )
        state["final_report"] = f"Misión de la División de Turismo completada.\nResumen de Operaciones:\n{report_body}"
    return state

def get_turismo_coronel_graph():
    workflow = StateGraph(TurismoColonelState)
    workflow.add_node("planner", create_tactical_plan)
    workflow.add_node("router", lambda state: state)
    workflow.add_node("prestadores_captain", prestadores_captain_node)
    workflow.add_node("compiler", compile_final_report)
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "router")
    workflow.add_conditional_edges(
        "router",
        route_to_captain,
        {
            "prestadores_captain": "prestadores_captain",
            "compile_report": "compiler",
            "route_to_captain": "router"
        }
    )
    workflow.add_edge("prestadores_captain", "router")
    workflow.add_edge("compiler", END)
    return workflow.compile()