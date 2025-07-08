from modules.llm_client import invoke_llm

def summarize_transcript(transcript, llm_type="ollama", api_key=None):
    prompt = f"""Summarize the following meeting transcript into key points:\n\n{transcript}"""
    return invoke_llm(prompt, llm_type=llm_type, api_key=api_key)
