# apps/llm-d-orchestrator/main.py
# This is the "brain" of our application. It takes a complex query,
# asks the LLM to decompose it, and then asks the LLM to solve each sub-problem.

import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Get the URL of the LLM service from an environment variable.
# In Kubernetes, this will be the name of the mock-llm-service.
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://mock-llm-service.llm-d-app.svc.cluster.local:8000")

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_complex_question(query: Query):
    """
    Main endpoint to handle a complex question using the LLM-D pattern.
    """
    print(f"Received complex question: {query.question}")

    # --- Step 1: Decompose the problem ---
    decomposition_prompt = f"Decompose this question into simple steps: '{query.question}'"
    print(f"Sending decomposition request to LLM: {decomposition_prompt}")

    try:
        async with httpx.AsyncClient() as client:
            # This call asks the LLM to act as a "Decomposer".
            response = await client.post(f"{LLM_SERVICE_URL}/generate", json={"prompt": decomposition_prompt})
            response.raise_for_status()
            sub_questions = response.json().get("response")
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        print(f"Error communicating with LLM service: {e}")
        raise HTTPException(status_code=500, detail="Failed to communicate with the LLM service.")

    if not isinstance(sub_questions, list):
        raise HTTPException(status_code=500, detail="LLM did not return a valid list of sub-questions.")

    print(f"LLM decomposed the problem into: {sub_questions}")

    # --- Step 2: Solve each sub-problem ---
    final_answers = []
    context = ""
    for sub_question in sub_questions:
        solving_prompt = f"Using this context: '{context}'. Answer this question: '{sub_question}'"
        print(f"Sending solving request to LLM for: {sub_question}")

        try:
            async with httpx.AsyncClient() as client:
                # This call asks the LLM to solve one simple step.
                response = await client.post(f"{LLM_SERVICE_URL}/generate", json={"prompt": solving_prompt})
                response.raise_for_status()
                answer = response.json().get("response")
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            raise HTTPException(status_code=500, detail="Failed to solve a sub-problem.")

        print(f"LLM answered: {answer}")
        final_answers.append({"question": sub_question, "answer": answer})
        # Build context for the next step
        context += f" {answer}"

    return {
        "original_question": query.question,
        "steps": final_answers
    }