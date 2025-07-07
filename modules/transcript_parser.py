import webvtt
import docx
import os

def extract_transcript(file_path: str) -> str:
    """ Extract transcript text from VTT or DOCX files """

    transcript_text = ""

    try:
        if file_path.endswith(".vtt"):
            transcript_text = extract_from_vtt(file_path)

        elif file_path.endswith(".docx"):
            transcript_text = extract_from_docx(file_path)

        else:
            raise ValueError("Unsupported file format! Please upload a .vtt or .docx file.")

    except Exception as e:
        return f"Error extracting transcript: {str(e)}"

    return transcript_text


def extract_from_vtt(file_path: str) -> str:
    """ Extracts transcript text from VTT (WebVTT) format """
    text = []
    try:
        for caption in webvtt.read(file_path):
            text.append(caption.text)
        return "\n".join(text)
    except Exception as e:
        return f"Error parsing VTT: {str(e)}"


def extract_from_docx(file_path: str) -> str:
    """ Extracts transcript text from DOCX file """
    text = []
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text.append(para.text)
        return "\n".join(text)
    except Exception as e:
        return f"Error parsing DOCX: {str(e)}"
