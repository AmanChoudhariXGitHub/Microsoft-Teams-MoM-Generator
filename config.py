import os

# === LLM Model Configurations ===

# Ollama (Local) model
OLLAMA_MODEL = "llama3.2:1b"

# OpenAI GPT model
OPENAI_MODEL = "gpt-3.5-turbo"

# Groq Cloud model
GROQ_MODEL = "mixtral-8x7b-32768"  # Alternatives: "llama3-70b-8192", "gemma-7b-it"

# === File Handling Configurations ===

UPLOAD_FOLDER = "uploads/"
DOWNLOAD_FOLDER = "downloads/"
ALLOWED_EXTENSIONS = {"vtt", "docx"}
