EXCEL_PROBLEMS = [
    {
        "id": "warmup",
        "question": "How would you clean a messy sales dataset with duplicates, inconsistent dates, and missing values?",
        "expected_skills": ["data_cleaning", "remove_duplicates", "text_to_columns", "power_query"]
    },
    {
        "id": "core1",
        "question": "How would you build a dynamic monthly sales dashboard that auto-updates when new data is added?",
        "expected_skills": ["pivot_tables", "dynamic_named_ranges", "charts", "power_query"]
    },
    {
        "id": "core2",
        "question": "A manager says their pivot table shows incorrect totals. What steps would you take to diagnose and fix it?",
        "expected_skills": ["pivot_table_troubleshooting", "data_types", "calculated_fields", "summarize_by"]
    },
    {
        "id": "curveball",
        "question": "What if this dataset had 2 million rows and needed to refresh every hour? How would you optimize?",
        "expected_skills": ["power_query_optimization", "connection_management", "external_data", "automation", "dax"]
    }
]

# NEW: Pre-interview questions (before Excel)
PRE_INTERVIEW_QUESTIONS = [
    {
        "id": "name",
        "question": "What's your full name?",
        "is_pre_interview": True
    },
    {
        "id": "about_you",
        "question": "Tell me about yourself — your background, experience, and why you're interested in this role.",
        "is_pre_interview": True
    }
]

ALL_QUESTIONS = PRE_INTERVIEW_QUESTIONS + EXCEL_PROBLEMS

SKILL_LEVEL_THRESHOLDS = {
    "beginner": (0, 30),
    "intermediate": (31, 60),
    "advanced": (61, 100)
}