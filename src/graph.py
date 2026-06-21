"""
Menyusun LangGraph: menghubungkan 4 node menjadi satu alur kerja
(workflow) yang linear: ekstrak -> filter -> ranking -> tulis rekomendasi.
"""

from langgraph.graph import StateGraph, END
from src.state import CarAdvisorState
from src.nodes import (
    node_ekstrak_kebutuhan,
    node_filter_kandidat,
    node_ranking,
    node_tulis_rekomendasi,
)


def build_graph():
    workflow = StateGraph(CarAdvisorState)

    # Daftarkan semua node
    workflow.add_node("ekstrak_kebutuhan", node_ekstrak_kebutuhan)
    workflow.add_node("filter_kandidat", node_filter_kandidat)
    workflow.add_node("ranking", node_ranking)
    workflow.add_node("tulis_rekomendasi", node_tulis_rekomendasi)

    # Titik masuk graph
    workflow.set_entry_point("ekstrak_kebutuhan")

    # Hubungkan node secara berurutan (edges)
    workflow.add_edge("ekstrak_kebutuhan", "filter_kandidat")
    workflow.add_edge("filter_kandidat", "ranking")
    workflow.add_edge("ranking", "tulis_rekomendasi")
    workflow.add_edge("tulis_rekomendasi", END)

    return workflow.compile()