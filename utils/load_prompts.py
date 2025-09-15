import os

def load_prompt(file_name):
    """
    Load a prompt text file from the 'prompts/' directory.
    Works regardless of where script is executed from.
    """
    # Navigate up to project root (where prompts/ lives)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(project_root, "prompts", file_name)

    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()