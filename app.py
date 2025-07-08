import streamlit as st
from models.mom_state import MeetingMinutesState
from utils.file_handler import save_uploaded_file, export_to_pdf, export_to_docx
from modules.transcript_parser import extract_transcript
from modules.summarizer import summarize_transcript
from modules.mom_generator import generate_mom
from modules.reviser import revise_mom

st.set_page_config(page_title="Teams MoM Generator", layout="wide")

st.title("📋 Microsoft Teams MoM Generator")

# Caching functions to prevent reprocessing
@st.cache_data
def process_transcript(file_path, llm_type, api_key):
    """ Extracts transcript, generates summary & MoM using selected LLM """
    transcript = extract_transcript(file_path)

    if llm_type in ["openai", "groq"] and not api_key:
        st.error("⚠️ Please enter a valid API Key.")
        return "", "", ""

    summary = summarize_transcript(transcript, llm_type=llm_type, api_key=api_key)
    mom = generate_mom(transcript, llm_type=llm_type, api_key=api_key)

    return transcript, summary, mom

@st.cache_data
def get_pdf(mom_text):
    return export_to_pdf(mom_text)

@st.cache_data
def get_docx(mom_text):
    return export_to_docx(mom_text)

# ---------------------- UI Controls ------------------------

# Select LLM Model
llm_option = st.selectbox("Choose AI Model", ["Ollama (Local)", "OpenAI GPT", "Groq Cloud"])

api_key = ""
if llm_option == "OpenAI GPT":
    api_key = st.text_input("🔑 Enter OpenAI API Key", type="password")
    llm_type = "openai"
elif llm_option == "Groq Cloud":
    api_key = st.text_input("🔑 Enter Groq API Key", type="password")
    llm_type = "groq"
else:
    llm_type = "ollama"

# Upload Transcript
uploaded_file = st.file_uploader("📂 Upload Teams Transcript (VTT/DOCX)", type=["vtt", "docx"])

# -------------------- Processing Flow ----------------------

if uploaded_file:
    st.info("Processing transcript... please wait.")
    file_path = save_uploaded_file(uploaded_file)
    state: MeetingMinutesState = {"file_path": file_path}

    try:
        state["transcript"], state["summary"], state["mom"] = process_transcript(file_path, llm_type, api_key)
    except Exception as e:
        st.error(f"❌ Error during processing: {e}")

    # Display Summary
    with st.expander("📄 **Generated Summary**", expanded=True):
        st.markdown(f"<div style='text-align: justify;'>{state['summary']}</div>", unsafe_allow_html=True)

    # Display MoM
    with st.expander("📝 **Generated Meeting Minutes**", expanded=True):
        st.markdown(f"<div style='text-align: justify;'>{state['mom']}</div>", unsafe_allow_html=True)

    # Feedback + Revise
    feedback = st.text_area("💡 Provide feedback for revision:")
    if st.button("🔄 Revise MoM"):
        state["human_feedback"] = feedback
        state["mom"] = revise_mom(state["mom"], feedback, llm_type=llm_type, api_key=api_key)
        with st.expander("📝 **Revised Meeting Minutes**", expanded=True):
            st.markdown(f"<div style='text-align: justify;'>{state['mom']}</div>", unsafe_allow_html=True)
        st.info("You can provide additional feedback and revise again if needed.")

    # Download Buttons
    col1, col2 = st.columns(2)

    with col1:
        pdf_path = get_pdf(state["mom"])
        with open(pdf_path, "rb") as pdf_file:
            st.download_button("📥 Download as PDF", pdf_file, file_name="Meeting_Minutes.pdf", mime="application/pdf")

    with col2:
        docx_path = get_docx(state["mom"])
        with open(docx_path, "rb") as docx_file:
            st.download_button("📥 Download as DOCX", docx_file, file_name="Meeting_Minutes.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
