# utils/report_generator.py

from utils.openrouter_client import call_openrouter
from utils.load_prompts import load_prompt
from ai_agent.knowledge import SKILL_LEVEL_THRESHOLDS


REPORT_PROMPT_TEMPLATE = load_prompt("generate_report.txt")


def generate_report(interview_history, scores):
    """
    Generates a personalized, accurate performance report.
    Returns dict with: report (str), overall_score, level, candidate_name
    """
    # Extract candidate name
    candidate_name = "Candidate"
    for qna in interview_history:
        if qna.get("is_pre_interview") and "name" in qna["question"].lower():
            candidate_name = qna["answer"].strip()
            break

    # Format interview history
    history_str = ""
    for i, qna in enumerate(interview_history):
        if not qna.get("is_pre_interview"):
            history_str += f"\nQ{i+1}: {qna['question']}\nA{i+1}: {qna['answer']}\n"

    # Format scores
    scores_str = "\n".join([f"Q{i+1}: {score}/25" for i, score in enumerate(scores)])

    # Prompt with context
    prompt = REPORT_PROMPT_TEMPLATE.format(
        interview_history=history_str,
        scores=scores_str,
        candidate_name=candidate_name
    )

    # Call OpenRouter
    response = call_openrouter(prompt, temperature=0.1, max_tokens=800)

    # Clean up response: remove extra whitespace and ensure it's text
    report_text = response.strip()

    # Determine overall level
    total_score = sum(scores)
    level = "beginner"
    for lvl, (min_s, max_s) in SKILL_LEVEL_THRESHOLDS.items():
        if min_s <= total_score <= max_s:
            level = lvl
            break

    return {
        "report": report_text,
        "overall_score": total_score,
        "level": level,
        "candidate_name": candidate_name
    }