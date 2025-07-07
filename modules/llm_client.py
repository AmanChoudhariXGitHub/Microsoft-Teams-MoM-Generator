import openai
from langchain_community.llms import Ollama
from config import OLLAMA_MODEL,OPENAI_MODEL

# Initialize Ollama model
ollama_llm = Ollama(model=OLLAMA_MODEL)

def invoke_openai(prompt, api_key):
    """ Calls OpenAI API"""
    try:
        # Initialize the OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Create a chat completion request
        response = client.chat.completions.create(
            model=OPENAI_MODEL, 
            messages=[
                {"role": "system", "content": "Generate structured output from transcript."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract and return the content of the assistant's response
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI Error: {str(e)}"

def invoke_ollama(prompt):
    """ Calls Ollama LLM to process the given prompt """
    return ollama_llm.invoke(prompt)

def invoke_llm(prompt, use_openai=False, api_key=None):
    """ Unified function to invoke either OpenAI or Ollama """
    if use_openai:
        if not api_key:
            raise ValueError("API key is required when using OpenAI.")
        return invoke_openai(prompt, api_key)
    return invoke_ollama(prompt)