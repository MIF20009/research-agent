from langgraph.graph import StateGraph, END

from src.app.graph.state import AgentState
from src.app.agents.retriever import retriever_agent
from src.app.agents.extractor import extractor_agent
from src.app.agents.synthesizer import synthesizer_agent


def build_lit_review_graph():
    g = StateGraph(AgentState)

    g.add_node("retriever", retriever_agent)
    g.add_node("extractor", extractor_agent)
    g.add_node("synthesizer", synthesizer_agent)

    # Entry point: start with a decision node
    def _route_entry(state: AgentState) -> str:
        """Route to extractor if papers uploaded, otherwise retriever"""
        if state.get("upload_papers") and state.get("papers"):
            return "extractor"
        return "retriever"
    
    g.set_entry_point("retriever")
    
    # From retriever to extractor
    g.add_edge("retriever", "extractor")
    
    # From extractor to synthesizer
    g.add_edge("extractor", "synthesizer")
    
    # From synthesizer to END
    g.add_edge("synthesizer", END)

    return g.compile()
