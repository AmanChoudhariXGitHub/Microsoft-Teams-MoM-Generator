# 📋 Microsoft Teams MoM Generator

🚀 **Automate Meeting Minutes (MoM) generation from Microsoft Teams effortlessly!**  
This application extracts transcripts from Microsoft Teams (`.vtt` / `.docx`), generates a structured **Summary** and **Meeting Minutes**, and allows exporting to **PDF** or **DOCX** format.

🟢 **Live App**: [ms-teams-mom-generator.streamlit.app](https://ms-teams-mom-generator.streamlit.app/)

---

## 🛠️ Features

✅ Upload Microsoft Teams transcripts (VTT / DOCX)  
✅ AI-Powered Summarization using **Ollama** (local) or **OpenAI GPT** (cloud)  
✅ Generates structured **Meeting Minutes** including:
- 🗣️ Discussion Points
- ✅ Action Items (Owner, Due Date)
- 🪜 Next Steps  

✅ Editable MoM with feedback-driven revision  
✅ Download as **PDF** or **DOCX**  
✅ Optimized with **caching** for faster processing

---

## 🚀 Installation & Setup (Local)

### 1️⃣ Clone the Repository

git clone https://github.com/AmanChoudhariXGitHub/Microsoft-Teams-MoM-Generator
cd Microsoft-Teams-MoM-Generator
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run the Application
streamlit run app.py

📂 Project Structure
TeamsMoMGenerator/
│
├── app.py                  # Streamlit app UI
├── requirements.txt        # Python dependencies
├── config.py               # LLM model configuration
├── README.md               # Project documentation
│
├── modules/
│   ├── transcript_parser.py   # Extracts text from VTT/DOCX
│   ├── summarizer.py          # AI-based summarization logic
│   ├── mom_generator.py       # Structured MoM generation
│   ├── reviser.py             # Revises MoM using feedback
│   └── llm_client.py          # Handles OpenAI/Ollama API calls
│
├── utils/
│   └── file_handler.py        # Uploads & export to PDF/DOCX
│
└── models/
    └── mom_state.py           # Tracks state across transcript, summary, MoM


⚡ How to Use
📂 Upload Transcript

Upload .vtt or .docx file from Microsoft Teams

🤖 Choose AI Model

Default: Ollama (runs locally)

Optional: OpenAI GPT (enter API key in sidebar)

📄 View Outputs

Summary: Key points from the meeting

Meeting Minutes:

Discussion Points

Action Items (with owner & deadline)

Next Steps

📝 Revise MoM

Provide feedback → get an improved version

📥 Download Results

Download as PDF or DOCX

🔐 OpenAI Key (Optional)
To use OpenAI GPT:

Add your API key in the app sidebar or use Streamlit Secrets.

In code:
import streamlit as st
import openai
openai.api_key = st.secrets["OPENAI_API_KEY"]
🧠 Model Options
Model	Source	Notes
Ollama	Local LLM	Fast and private (no API)
OpenAI	Cloud API	Better accuracy, needs key

🧑‍💻 Author
Aman Choudhari
GitHub: @AmanChoudhariXGitHub

🪪 License
This project is licensed under the MIT License.

