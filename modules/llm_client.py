import openai
import os
from langchain_community.llms import Ollama
from config import OLLAMA_MODEL, OPENAI_MODEL, GROQ_MODEL

ollama_llm = Ollama(model=OLLAMA_MODEL)

def invoke_openai(prompt, api_key):
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Generate structured output from transcript."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI Error: {str(e)}"
    
def invoke_ollama(prompt):
    """ Calls Ollama LLM to process the given prompt """
    return ollama_llm.invoke(prompt)

def invoke_groq(prompt, api_key):
    try:
        openai.api_key = api_key
        openai.api_base = "https://api.groq.com/openai/v1"

        response = openai.ChatCompletion.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Generate structured output from transcript."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Groq Error: {str(e)}"

def invoke_llm(prompt, llm_type="ollama", api_key=None):
    """ Unified function to invoke LLMs based on type """
    if llm_type == "openai":
        if not api_key:
            raise ValueError("OpenAI API key required.")
        return invoke_openai(prompt, api_key)
    elif llm_type == "groq":
        if not api_key:
            raise ValueError("Groq API key required.")
        return invoke_groq(prompt, api_key)
    else:
        return invoke_ollama(prompt)
