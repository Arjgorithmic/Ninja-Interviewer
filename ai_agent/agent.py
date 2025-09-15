from utils.load_prompts import load_prompt
from ai_agent.knowledge import ALL_QUESTIONS, PRE_INTERVIEW_QUESTIONS, EXCEL_PROBLEMS


INTERVIEW_FLOW_PROMPT = load_prompt("interview_flow.txt")


class ExcelInterviewerAgent:
    def __init__(self):
        self.questions = ALL_QUESTIONS
        self.current_step = 0
        self.answers = []  # List of dicts: {question, answer, is_pre_interview}
        self.state = "waiting_for_start"  # waiting_for_start | interviewing | completed

    def get_next_prompt(self):
        """Returns the next message to show the user."""
        if self.state == "waiting_for_start":
            return INTERVIEW_FLOW_PROMPT

        elif self.state == "interviewing" and self.current_step < len(self.questions):
            return self.questions[self.current_step]["question"]

        elif self.state == "completed":
            return "Interview complete. Generating your feedback report..."

        else:
            return "Unexpected state."

    def process_user_input(self, user_input):
        """Handles user input and advances state."""
        if self.state == "waiting_for_start":
            self.state = "interviewing"
            self.current_step = 0
            return "Understood. Let's begin."

        elif self.state == "interviewing" and self.current_step < len(self.questions):
            question_obj = self.questions[self.current_step]
            question_text = question_obj["question"]
            is_pre_interview = question_obj.get("is_pre_interview", False)

            # Save answer
            self.answers.append({
                "question": question_text,
                "answer": user_input,
                "is_pre_interview": is_pre_interview
            })

            # Advance to next question
            self.current_step += 1

            # If all questions done, mark as completed
            if self.current_step >= len(self.questions):
                self.state = "completed"
                return "Thank you for completing the assessment. I'll now generate your personalized feedback report."

            # Otherwise, return next question
            return self.get_next_prompt()

        elif self.state == "completed":
            return "Interview finished. Type 'restart' to begin again."

        return "Unexpected state."