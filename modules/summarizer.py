from modules.llm_client import invoke_openai, invoke_ollama

def summarize_transcript(transcript, use_openai=False, api_key=None):
    """ Summarizes transcript using the selected LLM """
    
    prompt = f"""
    Summarize the following meeting transcript into key points:

    {transcript}

    Ensure clarity, concise structure, and keep important decisions & action items.
    """

    if use_openai:
        return invoke_openai(prompt, api_key)
    
    return invoke_ollama(prompt)
