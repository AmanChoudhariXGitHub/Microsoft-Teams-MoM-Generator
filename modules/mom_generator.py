from modules.llm_client import invoke_openai, invoke_ollama

def generate_mom(transcript, use_openai=False, api_key=None):
    """ Generate structured Meeting Minutes using OpenAI or Ollama """

    prompt = f"""
    Convert the following meeting transcript into structured Meeting Minutes (MoM):

    {transcript}

    The MoM should include:
    - **Meeting Details** (Date, Time, Participants)
    - **Discussion Points** (Key technical & business discussions)
    - **Action Items** (Task, Owner, Due Date)
    - **Next Steps** (Follow-up tasks)

    Ensure the output is structured, professional, and properly formatted.
    """

    if use_openai:
        return invoke_openai(prompt, api_key)

    return invoke_ollama(prompt)
