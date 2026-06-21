"""
Definisi State (struktur data) yang mengalir di seluruh LangGraph.
State ini dibawa dan diperbarui oleh setiap node dalam graph.
"""

from typing import TypedDict, List, Optional


class CarAdvisorState(TypedDict):
    """
    State utama untuk graph Simple Car Advisor.

    Setiap field akan diisi/diperbarui oleh node yang berbeda:
    - user_input       -> diisi di awal (input dari user)
    - budget           -> diisi oleh node ekstrak_kebutuhan
    - kebutuhan        -> diisi oleh node ekstrak_kebutuhan
    - kandidat         -> diisi oleh node filter_kandidat
    - ranking          -> diisi oleh node ranking
    - rekomendasi_akhir-> diisi oleh node tulis_rekomendasi
    """
    user_input: str
    budget: Optional[int]
    kebutuhan: Optional[str]
    kandidat: List[dict]
    ranking: List[dict]
    rekomendasi_akhir: str