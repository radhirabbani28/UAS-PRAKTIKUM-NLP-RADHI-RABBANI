"""
Berisi seluruh LangChain prompt template & chain yang dipakai sistem.
LLM yang dipakai: Groq (gratis) dengan model Llama 3.3 70B.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

# Inisialisasi LLM dari Groq (gratis, cepat)
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)

# ============================================================
# CHAIN 1: Ekstrak budget & kebutuhan dari kalimat bebas user
# ============================================================
extract_prompt = ChatPromptTemplate.from_template("""
Kamu adalah sistem ekstraksi informasi. Ekstrak informasi dari kalimat
user berikut menjadi JSON dengan field:
- budget (angka dalam Rupiah, contoh: "150 juta" -> 150000000)
- kebutuhan (ringkasan singkat kebutuhan user, contoh: "keluarga, irit BBM")

Input user: {user_input}

PENTING: Jawab HANYA dengan JSON valid, tanpa penjelasan tambahan,
tanpa markdown code block.

Contoh output:
{{"budget": 150000000, "kebutuhan": "mobil keluarga, irit BBM"}}
""")
extract_kebutuhan_chain = extract_prompt | llm | JsonOutputParser()


# ============================================================
# CHAIN 2: Bandingkan & ranking kandidat mobil
# ============================================================
rank_prompt = ChatPromptTemplate.from_template("""
Kamu adalah penasihat mobil bekas yang ahli.

Kebutuhan user: "{kebutuhan}"

Berikut daftar kandidat mobil yang sesuai budget:
{kandidat}

Tugas kamu: pilih dan urutkan maksimal 3 mobil TERBAIK yang paling sesuai
dengan kebutuhan user di atas.

PENTING: Jawab HANYA dengan JSON list valid, tanpa penjelasan tambahan,
tanpa markdown code block. Format setiap item:
{{"id": <id_mobil>, "merek": "...", "model": "...", "alasan_singkat": "..."}}
""")
rank_chain = rank_prompt | llm | JsonOutputParser()


# ============================================================
# CHAIN 3: Tulis rekomendasi akhir dalam bahasa natural
# ============================================================
write_prompt = ChatPromptTemplate.from_template("""
Kamu adalah asisten penjual mobil bekas yang ramah dan komunikatif.

Budget user: Rp{budget}
Kebutuhan user: {kebutuhan}
Mobil-mobil pilihan terbaik: {ranking}

Tulis rekomendasi dalam bahasa Indonesia yang natural dan ramah,
maksimal 2 paragraf. Jelaskan kenapa tiap mobil cocok untuk kebutuhan user,
gunakan gaya bahasa seperti sedang ngobrol santai dengan calon pembeli.
""")
write_recommendation_chain = write_prompt | llm | StrOutputParser()