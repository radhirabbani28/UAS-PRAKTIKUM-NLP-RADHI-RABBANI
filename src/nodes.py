"""
Berisi 4 node utama yang menyusun alur kerja (workflow) LangGraph.
"""

import json
import os
from src.chains import (
    extract_kebutuhan_chain,
    rank_chain,
    write_recommendation_chain,
)

# Path data mobil (relatif terhadap root project)
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "mobil.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    DATA_MOBIL = json.load(f)


def node_ekstrak_kebutuhan(state):
    """
    Node 1: Menggunakan LLM (lewat LangChain) untuk mengekstrak
    budget dan kebutuhan dari kalimat bebas user.
    """
    result = extract_kebutuhan_chain.invoke({"user_input": state["user_input"]})
    return {
        "budget": result["budget"],
        "kebutuhan": result["kebutuhan"],
    }


def node_filter_kandidat(state):
    """
    Node 2: Filter mobil dari data berdasarkan budget user.
    Murni logika Python (rule-based), tidak memanggil LLM,
    supaya hemat token & cepat.
    """
    budget = state["budget"]
    toleransi = budget * 1.1  # beri toleransi 10% di atas budget

    kandidat = [mobil for mobil in DATA_MOBIL if mobil["harga"] <= toleransi]

    # Fallback: kalau tidak ada kandidat sama sekali, ambil 5 termurah
    if not kandidat:
        kandidat = sorted(DATA_MOBIL, key=lambda m: m["harga"])[:5]

    return {"kandidat": kandidat}


def node_ranking(state):
    """
    Node 3: LLM membandingkan kandidat dan memilih 3 mobil terbaik
    sesuai kebutuhan user.
    """
    result = rank_chain.invoke({
        "kebutuhan": state["kebutuhan"],
        "kandidat": json.dumps(state["kandidat"], ensure_ascii=False),
    })
    return {"ranking": result}


def node_tulis_rekomendasi(state):
    """
    Node 4: LLM menulis rekomendasi akhir dalam bahasa natural
    berdasarkan hasil ranking.
    """
    result = write_recommendation_chain.invoke({
        "budget": f"{state['budget']:,}".replace(",", "."),
        "kebutuhan": state["kebutuhan"],
        "ranking": json.dumps(state["ranking"], ensure_ascii=False),
    })
    return {"rekomendasi_akhir": result}