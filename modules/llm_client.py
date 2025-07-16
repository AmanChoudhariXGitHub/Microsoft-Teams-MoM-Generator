import openai
import os
from langchain_community.llms import Ollama
from config import OLLAMA_MODEL, OPENAI_MODEL, GROQ_MODEL, GROQ_API_KEY

# Import Groq SDK
from groq import Groq

# Initialize Ollama
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
    try:
        return ollama_llm.invoke(prompt)
    except Exception as e:
        return f"Ollama Error: {str(e)}"

def invoke_groq(prompt, api_key=None):
    try:
        # Fix: Groq client initialization - pass api_key as keyword argument
        if api_key is None:
            api_key = GROQ_API_KEY
            
        client = Groq(api_key=api_key)  # Fixed: use keyword argument
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Generate structured output from transcript."},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Groq Error: {str(e)}"

def invoke_llm(prompt, llm_type="ollama", api_key=None):
    if llm_type == "openai":
        if not api_key:
            raise ValueError("OpenAI API key required.")
        return invoke_openai(prompt, api_key)
    elif llm_type == "groq":
        return invoke_groq(prompt, api_key)
    else:
        return invoke_ollama(prompt)
