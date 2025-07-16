import streamlit as st
from models.mom_state import MeetingMinutesState
from utils.file_handler import save_uploaded_file, export_to_pdf, export_to_docx
from modules.transcript_parser import extract_transcript
from modules.summarizer import summarize_transcript
from modules.mom_generator import generate_mom, generate_summary_table, extract_speaker_analysis, extract_action_items_only
from modules.reviser import revise_mom

st.set_page_config(page_title="Teams MoM Generator", layout="wide", page_icon="📋")

st.title("📋 Microsoft Teams MoM Generator")
st.markdown("*Generate structured Meeting Minutes with Action Items and Discussion Tracking*")
st.markdown("---")

# Caching functions to prevent reprocessing
@st.cache_data
def process_transcript(file_path, llm_type, api_key):
    """ Extracts transcript, generates summary & MoM using selected LLM """
    transcript = extract_transcript(file_path)

    if llm_type in ["openai", "groq"] and not api_key:
        st.error("⚠️ Please enter a valid API Key.")
        return "", "", "", "", "", ""

    summary = summarize_transcript(transcript, llm_type=llm_type, api_key=api_key)
    mom = generate_mom(transcript, llm_type=llm_type, api_key=api_key)
    summary_table = generate_summary_table(transcript, llm_type=llm_type, api_key=api_key)
    speaker_analysis = extract_speaker_analysis(transcript, llm_type=llm_type, api_key=api_key)
    action_items = extract_action_items_only(transcript, llm_type=llm_type, api_key=api_key)

    return transcript, summary, mom, summary_table, speaker_analysis, action_items

@st.cache_data
def get_pdf(content):
    return export_to_pdf(content)

@st.cache_data
def get_docx(content):
    return export_to_docx(content)

# ---------------------- UI Controls ------------------------

# Create tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["🔧 Generate MoM", "📊 Summary Dashboard", "👥 Speaker Analysis", "✅ Action Items Tracker"])

with tab1:
    st.header("🔧 Meeting Minutes Generator")
    
    # Select LLM Model
    col1, col2 = st.columns([2, 1])
    
    with col1:
        llm_option = st.selectbox(
            "Choose AI Model", 
            ["Groq Cloud (Recommended)", "OpenAI GPT", "Ollama (Local)"],
            help="Select the AI model to process your transcript"
        )

    with col2:
        if llm_option.startswith("Ollama"):
            st.warning("⚠️ **Memory Issue Detected**: Your system may not have enough RAM for local models. Consider using Groq Cloud instead.")
        else:
            st.info("💡 **Tip**: Cloud models are faster and more reliable")

    api_key = ""
    if llm_option == "OpenAI GPT":
        api_key = st.text_input("🔑 Enter OpenAI API Key", type="password", help="Your OpenAI API key")
        llm_type = "openai"
    elif llm_option.startswith("Groq"):
        api_key = st.text_input("🔑 Enter Groq API Key", type="password", help="Your Groq API key", value="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")
        llm_type = "groq"
    else:
        llm_type = "ollama"
        st.info("🏠 Using local Ollama model - no API key required")
        st.warning("⚠️ **If you get memory errors**, please run: `ollama pull llama3.2:3b` in your terminal first")

    # Upload Transcript
    st.subheader("📂 Upload Meeting Transcript")
    uploaded_file = st.file_uploader(
        "Upload Teams Transcript (VTT/DOCX)", 
        type=["vtt", "docx"],
        help="Upload your Microsoft Teams meeting transcript file"
    )

    # -------------------- Processing Flow ----------------------

    if uploaded_file:
        with st.spinner("🔄 Processing transcript... please wait."):
            file_path = save_uploaded_file(uploaded_file)
            
            # Initialize session state
            if 'state' not in st.session_state:
                st.session_state.state = {"file_path": file_path}

            try:
                (st.session_state.state["transcript"], 
                 st.session_state.state["summary"], 
                 st.session_state.state["mom"],
                 st.session_state.state["summary_table"],
                 st.session_state.state["speaker_analysis"],
                 st.session_state.state["action_items"]) = process_transcript(file_path, llm_type, api_key)
                
                st.success("✅ Transcript processed successfully!")
                
            except Exception as e:
                st.error(f"❌ Error during processing: {e}")
                if "system memory" in str(e).lower():
                    st.error("💾 **Memory Issue**: Your system doesn't have enough RAM for the selected model.")
                    st.info("🔧 **Solutions**:")
                    st.info("1. Use Groq Cloud instead (recommended)")
                    st.info("2. Or run: `ollama pull llama3.2:3b` for a smaller model")
                    st.info("3. Or run: `ollama pull phi3:mini` for an even smaller model")

        # Display results in organized sections
        if 'state' in st.session_state and 'mom' in st.session_state.state and not st.session_state.state['mom'].startswith("Ollama Error"):
            
            # Main Meeting Minutes (Manager's requested format)
            st.subheader("📝 Official Meeting Minutes")
            st.info("📋 This format matches your manager's requirements")
            
            with st.container():
                st.markdown(st.session_state.state['mom'])

            # Quick Summary
            with st.expander("📄 **Quick Summary**", expanded=False):
                if not st.session_state.state['summary'].startswith("Ollama Error"):
                    st.markdown(st.session_state.state['summary'])
                else:
                    st.error("Summary generation failed due to model issues. Please try Groq Cloud.")

            # Feedback + Revise Section
            st.subheader("💡 Improve Meeting Minutes")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                feedback = st.text_area(
                    "Provide feedback for revision:",
                    placeholder="e.g., 'Add more details about the budget discussion' or 'Assign the API task to John instead of Sarah'"
                )
            
            with col2:
                st.markdown("**💡 Revision Tips:**")
                st.markdown("- Be specific about changes")
                st.markdown("- Mention names for reassignments")
                st.markdown("- Request additional details")
                
            if st.button("🔄 Revise MoM", type="primary"):
                if feedback:
                    with st.spinner("🔄 Revising based on your feedback..."):
                        st.session_state.state["human_feedback"] = feedback
                        revised_mom = revise_mom(
                            st.session_state.state["mom"], 
                            feedback, 
                            llm_type=llm_type, 
                            api_key=api_key
                        )
                        if not revised_mom.startswith("Ollama Error"):
                            st.session_state.state["mom"] = revised_mom
                            st.success("✅ MoM has been revised based on your feedback!")
                            st.markdown("### 📝 Revised Meeting Minutes")
                            st.markdown(st.session_state.state['mom'])
                        else:
                            st.error("Revision failed due to model issues. Please try Groq Cloud.")
                else:
                    st.warning("⚠️ Please provide feedback before revising.")

            # Download Buttons
            st.subheader("📥 Download Options")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                try:
                    pdf_path = get_pdf(st.session_state.state["mom"])
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            "📄 Download as PDF", 
                            pdf_file, 
                            file_name="Meeting_Minutes.pdf", 
                            mime="application/pdf",
                            use_container_width=True
                        )
                except:
                    st.error("PDF generation failed")

            with col2:
                try:
                    docx_path = get_docx(st.session_state.state["mom"])
                    with open(docx_path, "rb") as docx_file:
                        st.download_button(
                            "📝 Download as DOCX", 
                            docx_file, 
                            file_name="Meeting_Minutes.docx", 
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                except:
                    st.error("DOCX generation failed")
            
            with col3:
                # Copy to clipboard functionality
                st.markdown("📋 **Copy to Clipboard**")
                st.code(st.session_state.state["mom"], language="markdown")

        elif 'state' in st.session_state and 'mom' in st.session_state.state and st.session_state.state['mom'].startswith("Ollama Error"):
            st.error("❌ Model processing failed. Please try one of these solutions:")
            st.info("1. **Switch to Groq Cloud** (recommended - fastest and most reliable)")
            st.info("2. **Install smaller Ollama model**: Run `ollama pull llama3.2:3b`")
            st.info("3. **Or try even smaller**: Run `ollama pull phi3:mini`")

with tab2:
    st.header("📊 Meeting Summary Dashboard")
    
    if 'state' in st.session_state and 'summary_table' in st.session_state.state and not st.session_state.state['summary_table'].startswith("Ollama Error"):
        st.markdown(st.session_state.state['summary_table'])
        
        # Download summary table
        col1, col2 = st.columns(2)
        with col1:
            try:
                pdf_path = get_pdf(st.session_state.state["summary_table"])
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        "📥 Download Dashboard as PDF", 
                        pdf_file, 
                        file_name="Meeting_Summary_Dashboard.pdf", 
                        mime="application/pdf"
                    )
            except:
                st.error("PDF generation failed")
        
        with col2:
            try:
                docx_path = get_docx(st.session_state.state["summary_table"])
                with open(docx_path, "rb") as docx_file:
                    st.download_button(
                        "📥 Download Dashboard as DOCX", 
                        docx_file, 
                        file_name="Meeting_Summary_Dashboard.docx", 
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            except:
                st.error("DOCX generation failed")
    else:
        st.info("📋 Please upload and process a transcript in the 'Generate MoM' tab first.")

with tab3:
    st.header("👥 Speaker Analysis & Participation")
    
    if 'state' in st.session_state and 'speaker_analysis' in st.session_state.state and not st.session_state.state['speaker_analysis'].startswith("Ollama Error"):
        st.markdown(st.session_state.state['speaker_analysis'])
        
        # Download speaker analysis
        col1, col2 = st.columns(2)
        with col1:
            try:
                pdf_path = get_pdf(st.session_state.state["speaker_analysis"])
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        "📥 Download Analysis as PDF", 
                        pdf_file, 
                        file_name="Speaker_Analysis.pdf", 
                        mime="application/pdf"
                    )
            except:
                st.error("PDF generation failed")
        
        with col2:
            try:
                docx_path = get_docx(st.session_state.state["speaker_analysis"])
                with open(docx_path, "rb") as docx_file:
                    st.download_button(
                        "📥 Download Analysis as DOCX", 
                        docx_file, 
                        file_name="Speaker_Analysis.docx", 
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            except:
                st.error("DOCX generation failed")
    else:
        st.info("👥 Please upload and process a transcript in the 'Generate MoM' tab first.")

with tab4:
    st.header("✅ Action Items Tracker")
    
    if 'state' in st.session_state and 'action_items' in st.session_state.state and not st.session_state.state['action_items'].startswith("Ollama Error"):
        st.info("🎯 Focused view of all action items from the meeting")
        st.markdown(st.session_state.state['action_items'])
        
        # Download action items
        col1, col2 = st.columns(2)
        with col1:
            try:
                pdf_path = get_pdf(st.session_state.state["action_items"])
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        "📥 Download Action Items as PDF", 
                        pdf_file, 
                        file_name="Action_Items_Tracker.pdf", 
                        mime="application/pdf"
                    )
            except:
                st.error("PDF generation failed")
        
        with col2:
            try:
                docx_path = get_docx(st.session_state.state["action_items"])
                with open(docx_path, "rb") as docx_file:
                    st.download_button(
                        "📥 Download Action Items as DOCX", 
                        docx_file, 
                        file_name="Action_Items_Tracker.docx", 
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            except:
                st.error("DOCX generation failed")
    else:
        st.info("✅ Please upload and process a transcript in the 'Generate MoM' tab first.")

# Footer
st.markdown("---")
st.markdown("*Built for automated Meeting Minutes generation from Microsoft Teams transcripts*")
st.markdown("**Version 2.0** - Enhanced with manager-approved tabular format")
