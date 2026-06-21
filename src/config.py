"""
Setup environment variable untuk Groq API dan LangSmith tracing.
Pastikan file .env sudah diisi sebelum menjalankan aplikasi.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Aktifkan tracing LangSmith secara otomatis
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "simple-car-advisor"

# Validasi: pastikan API key tersedia
if not os.getenv("GROQ_API_KEY"):
    raise EnvironmentError(
        "GROQ_API_KEY tidak ditemukan. Pastikan file .env sudah diisi "
        "dengan API key dari https://console.groq.com"
    )

if not os.getenv("LANGCHAIN_API_KEY"):
    print(
        "[PERINGATAN] LANGCHAIN_API_KEY tidak ditemukan. "
        "Tracing LangSmith tidak akan berfungsi, tapi aplikasi tetap berjalan."
    )