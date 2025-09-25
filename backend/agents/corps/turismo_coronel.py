from typing import TypedDict, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from backend.agents.corps.units.prestadores_captain import get_prestadores_captain_graph

# --- DEFINICIÓN DEL ESTADO Y EL PLAN TÁCTICO DEL CORONEL ---
llm = ChatOpenAI(model="gpt-4o", temperature=0)

class CaptainTask(BaseModel):
    """Define una misión táctica clara para ser asignada a un Capitán."""
    task_description: str = Field(description="La descripción específica y detallada de la misión para el Capitán.")
    responsible_captain: str = Field(description="El Capitán especialista. Por ahora, solo 'Prestadores'.")

class TacticalPlan(BaseModel):
    """El plan táctico completo generado por el Coronel."""
    plan: List[CaptainTask] = Field(description="La lista de misiones tácticas secuenciales para cumplir la orden.")

class TurismoColonelState(TypedDict):
    """La pizarra táctica del Coronel de Turismo."""
    general_order: str
    tactical_plan: TacticalPlan | None
    task_queue: List[CaptainTask]
    completed_missions: list
    final_report: str
    error: str | None

# --- PUESTO DE MANDO: INSTANCIACIÓN DE CAPITANES ---
prestadores_captain_agent = get_prestadores_captain_graph()

# --- NODOS DEL GRAFO DE MANDO DEL CORONEL ---

async def create_tactical_plan(state: TurismoColonelState) -> TurismoColonelState:
    """
    (NODO 1: PLANIFICADOR TÁCTICO SIMULADO)
    En lugar de llamar a un LLM, devuelve un plan predefinido para la prueba.
    """
    print("--- 🧠 CORONEL DE TURISMO: Creando Plan Táctico (SIMULADO)... ---")

    # Simulamos el plan que el LLM debería generar.
    plan_simulado = TacticalPlan(plan=[
        CaptainTask(
            task_description=state['general_order'], # Pasamos la orden completa al Capitán
            responsible_captain='Prestadores'
        )
    ])

    print(f"--- 📝 CORONEL DE TURISMO: Plan Táctico Generado. Pasos: {len(plan_simulado.plan)} ---")
    state.update({
        "tactical_plan": plan_simulado,
        "task_queue": plan_simulado.plan.copy(),
        "completed_missions": [],
        "error": None
    })
    return state

def route_to_captain(state: TurismoColonelState):
    """(NODO 2: ENRUTADOR DE MANDO) Lee la siguiente misión en la cola y dirige el flujo."""
    if state.get("error") or not state["task_queue"]:
        return "compile_report"

    next_mission = state["task_queue"][0]
    captain_unit = next_mission.responsible_captain
    print(f"--- 🧭 CORONEL DE TURISMO: Enrutando misión a Capitán '{captain_unit}' ---")

    if captain_unit == 'Prestadores':
        return "prestadores_captain"
    else:
        state["error"] = f"Planificación defectuosa: Capitán desconocido '{captain_unit}'."
        state["task_queue"].pop(0)
        return "route_to_captain"

# --- NODO DE DELEGACIÓN DE MANDO (SUB-GRAFO) ---

async def prestadores_captain_node(state: TurismoColonelState) -> TurismoColonelState:
    """Invoca al sub-grafo del Capitán de Prestadores."""
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
    """(NODO FINAL: INFORME DE DIVISIÓN) Sintetiza todos los reportes."""
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

# --- ENSAMBLAJE DEL GRAFO DE MANDO DEL CORONEL ---

def get_turismo_coronel_graph():
    """Construye y compila el agente LangGraph para el Coronel de Turismo."""
    workflow = StateGraph(TurismoColonelState)

    workflow.add_node("planner", create_tactical_plan)
    workflow.add_node("router", lambda state: state) # Nodo 'passthrough'
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