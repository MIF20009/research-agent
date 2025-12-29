from langgraph.graph import StateGraph, END
from src.app.graph.state import AgentState

from src.app.agents.retriever import retriever_agent
from src.app.agents.extractor import extractor_agent
from src.app.agents.synthesizer import synthesizer_agent
from src.app.agents.hypothesis import hypothesis_agent


def build_lit_review_graph():
    g = StateGraph(AgentState)

    g.add_node("retriever", retriever_agent)
    g.add_node("extractor", extractor_agent)
    g.add_node("synthesizer", synthesizer_agent)
    g.add_node("hypothesis", hypothesis_agent)

    g.set_entry_point("retriever")
    g.add_edge("retriever", "extractor")
    g.add_edge("extractor", "synthesizer")
    g.add_edge("synthesizer", "hypothesis")
    g.add_edge("hypothesis", END)

    return g.compile()
