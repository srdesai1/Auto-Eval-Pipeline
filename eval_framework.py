import os
import csv
import time
import json
from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv


load_dotenv()

# 1. SETUP THE CLIENT
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    # Fallback for local testing if .env isn't used
    API_KEY = "PASTE_KEY_HERE_FOR_LOCAL_ONLY" 

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash-lite"

# 2. DEFINE THE OUTPUT STRUCTURE
class EvaluationScore(BaseModel):
    score: int = Field(description="An integer score from 1 to 5.")
    reasoning: str = Field(description="A 1-sentence explanation for the score.")

# 3. DEFINE THE JUDGE FUNCTION
def judge_response(prompt: str, ai_answer: str) -> dict:
    """Uses the LLM as a judge to grade an answer based on strict criteria."""
    
    judge_system_prompt = f"""
    You are an expert AI Evaluator. 
    Your job is to grade the AI's answer to the user's prompt.
    Score from 1 to 5 based on accuracy, conciseness, and helpfulness.
    1 = Terrible/Hallucinated, 5 = Perfect and concise.
    
    User Prompt: {prompt}
    AI Answer: {ai_answer}
    """
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=judge_system_prompt,
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=EvaluationScore,
            temperature=0.1 
        ),
    )
    
    return json.loads(response.text)

# 4. THE EXECUTION BLOCK
if __name__ == "__main__":
    print("__Starting the SentinEval Framework...\n")
    
    test_cases = [
        {
            "prompt": "Explain quantum computing to a 5 year old.",
            "test_answer": "Quantum computing uses qubits which can exist in superposition, allowing for parallel processing of complex algorithms." 
        },
        {
            "prompt": "What is 2 + 2?",
            "test_answer": "2 + 2 is 4." 
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases):
        print(f"Evaluating Test {i+1}...")
        
        try:
            eval_result = judge_response(test["prompt"], test["test_answer"])
            
            print(f"Prompt: {test['prompt']}")
            print(f"Score: {eval_result['score']}/5")
            print(f"Reason: {eval_result['reasoning']}\n")
            print("-" * 40 + "\n")
            
            results.append({
                "prompt": test["prompt"],
                "score": eval_result["score"],
                "reasoning": eval_result["reasoning"]
            })
        except Exception as e:
            print(f"Error evaluating test {i+1}: {e}")
        
        # Rate Limit Backoff: 5-second pause to prevent 429 Errors
        time.sleep(5) 

    # Save results to CSV
    with open('eval_results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["prompt", "score", "reasoning"])
        writer.writeheader()
        writer.writerows(results)
        
    print("Evals complete. Results saved to eval_results.csv")
