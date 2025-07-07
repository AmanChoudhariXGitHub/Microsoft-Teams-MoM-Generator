📋 Microsoft Teams MoM Generator
🚀 Automate Microsoft Teams Meeting Minutes (MoM) effortlessly!
    This application extracts transcripts from Microsoft Teams (VTT/DOCX) files, generates a structured Summary & Meeting Minutes, and allows exporting to PDF & DOCX.

    You can access this app on https://ms-teams-mom-generator.streamlit.app/

🛠 Features
✅ Upload Microsoft Teams transcripts (VTT/DOCX)
✅ AI-Powered Summarization using Ollama or OpenAI GPT
✅ Generates Structured Meeting Minutes (Discussion Points, Action Items, Next Steps)
✅ Editable MoM with Feedback & Revision
✅ Download MoM in PDF or DOCX format
✅ Optimized with Caching for Faster Processing

🚀 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/AmanChoudhariXGitHub/Microsoft-Teams-MoM-Generator
cd TeamsMoMGenerator
2️⃣ Install Dependencies

pip install -r requirements.txt
3️⃣ Run the Application

streamlit run app.py

📂 Project Structure

TeamsMoMGenerator/
│── app.py                   # Streamlit UI for the app
│── requirements.txt          # Required dependencies
│── modules/
│   ├── transcript_parser.py  # Extract transcript from VTT/DOCX
│   ├── summarizer.py         # Summarize transcript (supports OpenAI/Ollama)
│   ├── mom_generator.py      # Generate structured MoM (supports OpenAI/Ollama)
│   ├── reviser.py            # Revise MoM based on user feedback
│   ├── llm_client.py         # Handles OpenAI & Ollama interactions
│── utils/
│   ├── file_handler.py       # Handles file uploads & export (PDF/DOCX)
│── models/
│   ├── mom_state.py          # Manages state of transcript, summary & MoM
│── config.py                 # Configuration settings for LLM
│── README.md                 # Project documentation

⚡ Usage
1️⃣ Upload a Microsoft Teams Transcript
Click 📂 Upload Teams Transcript
Select a VTT/DOCX file from Microsoft Teams
2️⃣ Choose AI Model (Ollama or OpenAI)
Default: Uses Ollama (Runs locally)
Optionally: Use OpenAI GPT (Enter API Key)
3️⃣ View Summary & MoM
📄 Summary: Key points extracted from the meeting
📝 Meeting Minutes (MoM): Structured report with
Discussion Points
Action Items (Owner, Due Date)
Next Steps
4️⃣ Edit & Revise MoM (Optional)
Add feedback and Revise MoM
5️⃣ Download MoM as PDF or DOCX
Click 📥 Download as PDF or 📥 Download as DOCX