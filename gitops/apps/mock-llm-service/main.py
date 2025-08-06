# apps/mock-llm-service/main.py
# This is our mock LLM. It simulates the behavior of a real LLM by returning
# hard-coded responses based on keywords in the prompt.

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
async def generate(prompt: Prompt):
    """
    Simulates an LLM generating a response.
    In a real-world scenario, this would be a GPU-intensive service.
    """
    prompt_text = prompt.prompt.lower()
    print(f"Mock LLM received prompt: {prompt_text}")

    # --- Decomposer Logic ---
    if "decompose" in prompt_text and "florida" in prompt_text:
        # If asked to decompose our example question, return the steps.
        response = [
            "1. Find the capital of Florida.",
            "2. Find the current time in the capital.",
            "3. Determine if it is daytime or nighttime."
        ]
        print(f"Mock LLM is decomposing. Response: {response}")
        return {"response": response}

    # --- Solver Logic ---
    elif "capital of florida" in prompt_text:
        response = "The capital of Florida is Tallahassee."
        print(f"Mock LLM is solving. Response: {response}")
        return {"response": response}
    elif "time in tallahassee" in prompt_text:
        response = "The current time is 6:49 PM EDT."
        print(f"Mock LLM is solving. Response: {response}")
        return {"response": response}
    elif "daytime or nighttime" in prompt_text:
        response = "It is currently nighttime."
        print(f"Mock LLM is solving. Response: {response}")
        return {"response": response}

    # --- Fallback ---
    else:
        response = "I am a mock LLM and can only answer specific questions."
        print(f"Mock LLM fallback. Response: {response}")
        return {"response": response}