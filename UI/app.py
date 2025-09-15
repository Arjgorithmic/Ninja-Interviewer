# UI/app.py

import sys
import os
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from ai_agent.agent import ExcelInterviewerAgent
from ai_agent.evaluator import evaluate_answer
from utils.report_generator import generate_report
from ai_agent.knowledge import ALL_QUESTIONS, PRE_INTERVIEW_QUESTIONS, EXCEL_PROBLEMS

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "agent" not in st.session_state:
    st.session_state.agent = ExcelInterviewerAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "scores" not in st.session_state:
    st.session_state.scores = []
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False
if "candidate_name" not in st.session_state:
    st.session_state.candidate_name = "Candidate"

# --- HOME SCREEN ---
if st.session_state.page == "home":
    st.set_page_config(page_title="Ninja Interviewer", page_icon="🥷🏻")
    st.title("Ninja Interviewer")
    st.markdown("""
    AI-Powered Excel Mock Interviewer
    
    By:
        Name : Arjun P Dinesh
        Applying for : Gen AI Engineer role at Coding Ninjas
    

     Click below to begin your 10-minute mock interview.
    """)

    if st.button("Start Interview", type="primary", use_container_width=True):
        st.session_state.page = "interview"
        st.session_state.agent = ExcelInterviewerAgent()  # Reset agent
        st.session_state.messages = []  # Clear chat
        st.session_state.scores = []
        st.session_state.report_generated = False
        st.session_state.candidate_name = "Candidate"
        st.rerun()

# --- INTERVIEW SCREEN ---
else:
    st.set_page_config(page_title="Ninja Interviewer", page_icon="🥷🏻    ")

    # Add initial welcome message if this is the first turn
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "I'm Ninja Interviewer AI. I'll ask you a few personal questions to get to know you, followed by 4 real-world Excel problems. Answer as if you're in a live interview."
        })

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Handle user input
    if prompt := st.chat_input("Type your answer here..."):
        # Append user message immediately
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Extract candidate name from first response (only if it's the very first question)
        if len(st.session_state.messages) == 2:  # First user message after welcome
            first_question = st.session_state.agent.questions[0]["question"].lower()
            if "name" in first_question or "full name" in first_question:
                st.session_state.candidate_name = prompt.strip()
                # Update the displayed user message to show name clearly
                st.session_state.messages[-1]["content"] = f"Name: {prompt.strip()}"

        # Process input through agent
        agent_response = st.session_state.agent.process_user_input(prompt)

        # If interview completed, generate report
        if st.session_state.agent.state == "completed" and not st.session_state.report_generated:
            # Collect scores ONLY for Excel questions (skip pre-interview)
            excel_answers = [a for a in st.session_state.agent.answers if not a.get("is_pre_interview")]
            scores = []
            for qna in excel_answers:
                eval_result = evaluate_answer(qna["question"], qna["answer"])
                scores.append(eval_result["total_score"])
            st.session_state.scores = scores

            # Generate report with candidate name
            report_data = generate_report(excel_answers, scores)
            st.session_state.report = report_data
            st.session_state.report_generated = True

            # Display report
            # Create full report string with proper formatting
            full_report = (
                f"### 📄 Your Performance Report\n\n"
                f"**Candidate Name:** {report_data['candidate_name']}\n"
                f"**Overall Proficiency:** {report_data['level'].title()} ({report_data['overall_score']}/100)\n\n"
                f"{report_data['report']}"
            )

            # Display in chat message
            with st.chat_message("assistant"):
                st.markdown(full_report)

            # Save report message
            full_report_msg = (
                f"### 📄 Your Performance Report\n"
                f"**Candidate Name:** {report_data['candidate_name']}\n"
                f"**Overall Proficiency:** {report_data['level'].title()} ({report_data['overall_score']}/100)\n\n"
                f"{report_data['report']}"
            )
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_report_msg
            })

        else:
            # Append AI response immediately
            st.session_state.messages.append({"role": "assistant", "content": agent_response})

        # Force rerun to ensure immediate UI update
        st.rerun()

    # Restart button (appears only after interview completion)
    if st.session_state.agent.state == "completed":
        if st.button("Restart Interview", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()