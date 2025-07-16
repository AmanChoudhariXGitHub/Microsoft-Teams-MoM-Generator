import os
import webvtt
import docx

def extract_transcript(file_path: str) -> str:
    """
    Extract transcript text from VTT or DOCX file.
    Supported extensions: .vtt, .docx
    """
    try:
        if file_path.endswith(".vtt"):
            return extract_from_vtt(file_path)
        elif file_path.endswith(".docx"):
            return extract_from_docx(file_path)
        else:
            raise ValueError("❌ Unsupported file format! Please upload a .vtt or .docx file.")
    except Exception as e:
        return f"⚠️ Error extracting transcript: {str(e)}"

def extract_from_vtt(file_path: str) -> str:
    """Extracts transcript text from VTT (WebVTT) file."""
    try:
        text = [caption.text for caption in webvtt.read(file_path)]
        return "\n".join(text)
    except Exception as e:
        return f"⚠️ Error parsing VTT file: {str(e)}"

def extract_from_docx(file_path: str) -> str:
    """Extracts transcript text from DOCX file."""
    try:
        doc = docx.Document(file_path)
        text = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(text)
    except Exception as e:
        return f"⚠️ Error parsing DOCX file: {str(e)}"
