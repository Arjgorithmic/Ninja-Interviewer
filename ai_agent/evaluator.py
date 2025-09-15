# ai_agent/evaluator.py

from utils.openrouter_client import call_openrouter
from utils.load_prompts import load_prompt

EVAL_PROMPT_TEMPLATE = load_prompt("evaluate_answer.txt")


def evaluate_answer(question, answer):
    """
    Evaluates a candidate's answer using OpenRouter LLM.
    Returns dict: {accuracy, efficiency, depth, feedback, skill_level, total_score}
    """
    prompt = EVAL_PROMPT_TEMPLATE.format(question=question, answer=answer)

    response = call_openrouter(prompt, temperature=0.2, max_tokens=300)

    try:
        # Parse JSON from LLM output
        import json
        result = json.loads(response.strip())

        # Validate required keys
        required_keys = {"accuracy", "efficiency", "depth", "feedback", "skill_level"}
        if not required_keys.issubset(result.keys()):
            raise ValueError("Invalid response structure from LLM")

        # Map skill_level to our enum
        if result["skill_level"] not in ["beginner", "intermediate", "advanced"]:
            result["skill_level"] = "intermediate"

        # Calculate total score (out of 15 → scaled to 25)
        total_score = (result["accuracy"] + result["efficiency"] + result["depth"]) * (25 / 15)
        result["total_score"] = round(total_score, 1)

        return result

    except json.JSONDecodeError:
        return {
            "accuracy": 2,
            "efficiency": 2,
            "depth": 2,
            "feedback": "Could not parse response. Try being more specific in your explanation.",
            "skill_level": "beginner",
            "total_score": 10.0
        }
    except Exception as e:
        return {
            "accuracy": 2,
            "efficiency": 2,
            "depth": 2,
            "feedback": f"Error evaluating answer: {str(e)}. Please rephrase your answer.",
            "skill_level": "beginner",
            "total_score": 10.0
        }