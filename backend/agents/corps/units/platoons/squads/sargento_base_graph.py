from typing import TypedDict, Any, List, Annotated
import operator
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool

class SargentoBaseState(TypedDict):
    """La pizarra táctica estandarizada para todos los Sargentos."""
    teniente_order: str
    app_context: Any
    messages: Annotated[List[BaseMessage], operator.add]
    final_report: str
    error: str | None

class SargentoGraphBuilder:
    """Constructor estandarizado para todos los agentes Sargento."""

    def __init__(self, squad: List[BaseTool], squad_name: str):
        self.squad_executor = ToolNode(squad)
        self.squad_name = squad_name
        self.model = ChatOpenAI(model="gpt-4o-2024-05-13", temperature=0).bind_tools(squad)

    def get_sargento_brain(self, state: SargentoBaseState):
        """
        (CEREBRO REAL) El cerebro del Sargento. Analiza el estado y decide la siguiente acción para su escuadra.
        """
        print(f"--- 🤔 SARGENTO ({self.squad_name}): Analizando orden y decidiendo acción... ---")
        return self.model.invoke(state["messages"])

    def route_action(self, state: SargentoBaseState):
        """Revisa la decisión del cerebro y enruta al ejecutor o al informe final."""
        last_message = state["messages"][-1]
        if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
            return "compile_report"
        return "squad_executor"

    def compile_report_node(self, state: SargentoBaseState) -> SargentoBaseState:
        """Compila el informe final para el Teniente a partir del historial de la misión."""
        print(f"--- 📄 SARGENTO ({self.squad_name}): Misión completada. Compilando reporte. ---")

        # Extraemos el contenido del último mensaje de la IA como reporte.
        last_ai_message = state["messages"][-1].content
        report_body = last_ai_message if last_ai_message else "La escuadra ejecutó la misión sin un reporte verbal."

        state["final_report"] = f"Misión completada. Reporte de la escuadra de {self.squad_name}: {report_body}"
        return state

    def build_graph(self):
        """Construye y compila el grafo LangGraph para el Sargento."""
        workflow = StateGraph(SargentoBaseState)

        def mission_entry_node(state: SargentoBaseState):
            return {"messages": [HumanMessage(content=state["teniente_order"])]}

        workflow.add_node("mission_entry", mission_entry_node)
        workflow.add_node("brain", self.get_sargento_brain) # Usamos el cerebro real
        workflow.add_node("squad_executor", self.squad_executor)
        workflow.add_node("compiler", self.compile_report_node)

        workflow.add_edge(START, "mission_entry")
        workflow.add_edge("mission_entry", "brain")
        workflow.add_conditional_edges(
            "brain",
            self.route_action,
            {"squad_executor": "squad_executor", "compiler": "compiler"}
        )
        workflow.add_edge("squad_executor", "brain")
        workflow.add_edge("compiler", END)

        return workflow.compile()