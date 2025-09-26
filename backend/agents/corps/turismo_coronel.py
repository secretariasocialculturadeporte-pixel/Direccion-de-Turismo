from typing import TypedDict, List
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from importlib import import_module
from langchain_openai import ChatOpenAI

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
    print(f"--- 🧠 CORONEL: Planificando para la orden: '{state['general_order']}' ---")

    prompt = f"""
Eres el Coronel de Turismo, un experto en logística y delegación. Tu misión es analizar la orden de tu General y asignarla al Capitán especialista más adecuado.

Capitanes bajo tu mando y sus especialidades:
- Admin: Para aprobar, rechazar o moderar contenido.
- Turista: Para acciones de un turista, como guardar favoritos en "Mi Viaje".
- Funcionario: Para gestionar contenido institucional del municipio.
- Videos: Para añadir, eliminar o gestionar videos.
- Artesanos: Para registrar o gestionar perfiles de artesanos.
- Oferta: Para gestionar promociones, ofertas y paquetes especiales.
- Prestadores: Para todos los demás prestadores de servicios (hoteles, restaurantes, guías, agencias, transporte).
- Atractivos: Para crear o gestionar atractivos turísticos.
- Publicaciones: Para crear noticias, eventos o blogs.

Orden del General: "{state['general_order']}"

Crea un plan de un solo paso para el Capitán apropiado en formato JSON.
"""
    try:
        structured_llm = ChatOpenAI(model="gpt-4o", temperature=0).with_structured_output(TacticalPlan)
        plan = await structured_llm.ainvoke(prompt)
        state.update({"tactical_plan": plan, "task_queue": plan.plan.copy(), "completed_missions": []})
    except Exception as e:
        state["error"] = f"Error del LLM al planificar para el Coronel: {e}"
    return state

def route_to_captain(state: TurismoColonelState):
    if state.get("error") or not state["task_queue"]:
        return "compile_report"
    return f"{state['task_queue'][0].responsible_captain.lower()}_captain"

async def generic_captain_node(state: TurismoColonelState, captain_module_name: str, captain_graph_func: str, captain_name: str) -> TurismoColonelState:
    mission = state["task_queue"].pop(0)
    print(f"--- 🔽 CORONEL: Delegando a CAP. {captain_name.upper()} -> '{mission.task_description}' ---")
    try:
        module = import_module(f"agents.corps.units.{captain_module_name}")
        get_captain_graph = getattr(module, captain_graph_func)
        captain_agent = get_captain_graph()
        result = await captain_agent.ainvoke({"coronel_order": mission.task_description, "app_context": state.get("app_context")})
        state["completed_missions"].append({"captain": captain_name, "report": result.get("final_report", "Sin reporte.")})
    except Exception as e:
        state["error"] = f"Error al cargar o ejecutar el cuerpo del Capitán {captain_name}: {e}"
    return state

async def compile_final_report(state: TurismoColonelState) -> TurismoColonelState:
    if state.get("error"):
        state["final_report"] = f"Misión fallida. Razón: {state['error']}"
    else:
        report_body = "\n".join([f"- Reporte del Capitán de {m['captain']}:\n  {m['report']}" for m in state["completed_missions"]])
        state["final_report"] = f"Misión de la División de Turismo completada.\nResumen de Operaciones:\n{report_body}"
    return state

def get_turismo_coronel_graph():
    workflow = StateGraph(TurismoColonelState)
    workflow.add_node("planner", create_tactical_plan)
    workflow.add_node("router", lambda s: s)

    captain_nodes_map = {
        "prestadores_captain": ("prestadores_captain", "get_prestadores_captain_graph", "Prestadores"),
        "atractivos_captain": ("atractivos_captain", "get_atractivos_captain_graph", "Atractivos"),
        "publicaciones_captain": ("publicaciones_captain", "get_publicaciones_captain_graph", "Publicaciones"),
        "admin_captain": ("admin_captain", "get_admin_captain_graph", "Admin"),
        "turista_captain": ("turista_captain", "get_turista_captain_graph", "Turista"),
        "funcionario_captain": ("funcionario_captain", "get_funcionario_captain_graph", "Funcionario"),
        "videos_captain": ("videos_captain", "get_videos_captain_graph", "Videos"),
        "artesanos_captain": ("artesanos_captain", "get_artesanos_captain_graph", "Artesanos"),
        "oferta_captain": ("oferta_captain", "get_oferta_captain_graph", "Oferta"),
    }
    for node_name, (module, func, display) in captain_nodes_map.items():
        workflow.add_node(node_name, lambda s, m=module, f=func, d=display: generic_captain_node(s, m, f, d))

    workflow.add_node("compiler", compile_final_report)
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "router")

    conditional_map = {name: name for name in captain_nodes_map.keys()}
    conditional_map["compile_report"] = "compiler"
    workflow.add_conditional_edges("router", route_to_captain, conditional_map)

    for node_name in captain_nodes_map.keys():
        workflow.add_edge(node_name, "router")

    workflow.add_edge("compiler", END)
    return workflow.compile()