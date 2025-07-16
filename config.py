import os

# === LLM Model Configurations ===

# Ollama (Local) model - Using smaller model that requires less RAM
OLLAMA_MODEL = "qwen2:1.5b"  # This model requires only ~2GB RAM instead of 6GB

# Alternative smaller models you can try:
# OLLAMA_MODEL = "phi3:mini"      # Very small, ~2GB RAM
# OLLAMA_MODEL = "gemma2:2b"      # Even smaller, ~1.5GB RAM
# OLLAMA_MODEL = "qwen2:1.5b"     # Smallest option, ~1GB RAM

# OpenAI GPT model
OPENAI_MODEL = "gpt-3.5-turbo"

# Groq Cloud model
GROQ_MODEL = "mistral-saba-24b"  # You can also try "llama3-70b-8192" for better results

# Use environment variable for Groq API Key, with fallback to your provided key
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

# === File Handling Configurations ===

UPLOAD_FOLDER = "uploads/"
DOWNLOAD_FOLDER = "downloads/"
ALLOWED_EXTENSIONS = {"vtt", "docx"}

# === Meeting Minutes Configuration ===

# Default meeting minutes template structure
MOM_TEMPLATE_COLUMNS = ["Type", "Description", "Assignees", "Due", "Status"]
VALID_TYPES = ["Information", "Action"]
DEFAULT_STATUS = "Open"
