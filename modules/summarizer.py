from modules.llm_client import invoke_llm

def summarize_transcript(transcript, llm_type="ollama", api_key=None):
    """ Summarizes transcript using the selected LLM """
    
    prompt = f"""
    Summarize the following meeting transcript into key points:

    {transcript}

    Ensure clarity, concise structure, and keep important decisions & action items.
    """

    return invoke_llm(prompt, llm_type=llm_type, api_key=api_key)
