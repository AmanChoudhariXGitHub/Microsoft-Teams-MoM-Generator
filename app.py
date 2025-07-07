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
def process_transcript(file_path, use_openai, openai_api_key):
    """ Extracts transcript, generates summary & MoM using selected LLM """
    transcript = extract_transcript(file_path)

    if use_openai:
        if not openai_api_key:
            st.error("⚠️ Please enter a valid OpenAI API Key.")
            return "", "", ""
        summary = summarize_transcript(transcript, use_openai=True, api_key=openai_api_key)
        mom = generate_mom(transcript, use_openai=True, api_key=openai_api_key)
    else:
        summary = summarize_transcript(transcript, use_openai=False)
        mom = generate_mom(transcript, use_openai=False)

    return transcript, summary, mom

@st.cache_data
def get_pdf(mom_text):
    """ Generates and caches PDF file """
    return export_to_pdf(mom_text)

@st.cache_data
def get_docx(mom_text):
    """ Generates and caches DOCX file """
    return export_to_docx(mom_text)

# LLM Selection (Ollama or OpenAI)
use_openai = st.checkbox("Use OpenAI GPT (instead of Ollama)")

openai_api_key = ""
if use_openai:
    openai_api_key = st.text_input("🔑 Enter OpenAI API Key", type="password")

# Upload VTT/DOCX file
uploaded_file = st.file_uploader("📂 Upload Teams Transcript (VTT/DOCX)", type=["vtt", "docx"])


if uploaded_file:
    st.info("Processing transcript... please wait.")
    
    # Save file locally
    file_path = save_uploaded_file(uploaded_file)
    
    # Initialize state
    state: MeetingMinutesState = {"file_path": file_path}
    
    try:
        # Process transcript (cached)
        state["transcript"], state["summary"], state["mom"] = process_transcript(file_path, use_openai, openai_api_key)
        
    except Exception as e:
        st.error(f"❌ Error during processing: {e}")
    
    # Display Summary & MoM in Expanders
    with st.expander("📄 **Generated Summary**", expanded=True):
        st.markdown(f"<div style='text-align: justify;'>{state['summary']}</div>", unsafe_allow_html=True)

    with st.expander("📝 **Generated Meeting Minutes**", expanded=True):
        st.markdown(f"<div style='text-align: justify;'>{state['mom']}</div>", unsafe_allow_html=True)

    # Feedback Section
    feedback = st.text_area("💡 Provide feedback for revision:")
    if st.button("🔄 Revise MoM"):
        state["human_feedback"] = feedback
        state["mom"] = revise_mom(state["mom"])

        with st.expander("📝 **Revised Meeting Minutes**", expanded=True):
            st.markdown(f"<div style='text-align: justify;'>{state['mom']}</div>", unsafe_allow_html=True)
        st.info("You can provide additional feedback and revise again if needed.")

    # Add Download Buttons for PDF & DOCX
    col1, col2 = st.columns(2)

    with col1:
        pdf_path = get_pdf(state["mom"])
        with open(pdf_path, "rb") as pdf_file:
            st.download_button("📥 Download as PDF", pdf_file, file_name="Meeting_Minutes.pdf", mime="application/pdf")

    with col2:
        docx_path = get_docx(state["mom"])
        with open(docx_path, "rb") as docx_file:
            st.download_button("📥 Download as DOCX", docx_file, file_name="Meeting_Minutes.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
