import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.tools import (
    check_leave_balance,
    check_attendance,
    get_employee_details
)

from app.rag import search_hr_policy


# ==========================================
# 1. Find project folder
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# 2. Load .env
# ==========================================

load_dotenv(BASE_DIR / ".env")


# ==========================================
# 3. Get Groq API key
# ==========================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")


# ==========================================
# 4. Create AI model
# ==========================================

llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)


# ==========================================
# 5. Main AI function
# ==========================================

def ask_ai(message, employee_id):

    message_lower = message.lower().strip()


    # ======================================
    # LEAVE BALANCE
    # ======================================

    if "leave" in message_lower and (
        "balance" in message_lower
        or "remaining" in message_lower
        or "left" in message_lower
        or "how many" in message_lower
        or "how much" in message_lower
        or "days" in message_lower
    ):

        result = check_leave_balance(employee_id)


    # ======================================
    # ATTENDANCE
    # ======================================

    elif "attendance" in message_lower:

        result = check_attendance(employee_id)


    # ======================================
    # EMPLOYEE PROFILE
    # ======================================

    elif (
        "profile" in message_lower
        or "employee details" in message_lower
        or "my details" in message_lower
        or "my information" in message_lower
        or "about me" in message_lower
    ):

        result = get_employee_details(employee_id)


    # ======================================
    # HR POLICY / RAG
    # ======================================

    elif (
        "policy" in message_lower
        or "annual leave" in message_lower
        or "sick leave" in message_lower
        or "work from home" in message_lower
        or "working hours" in message_lower
        or "salary" in message_lower
    ):

        result = search_hr_policy(message)


    # ======================================
    # GENERAL AI QUESTION
    # ======================================

    else:

        response = llm.invoke(
            f"""
You are an AI HR Assistant.

Answer the employee's question clearly and briefly.

Employee question:
{message}

If the question requires personal employee information,
do not invent information.

If you do not have the required information,
clearly say that the information is not available.
"""
        )

        return response.content


    # ======================================
    # CONVERT SYSTEM RESULT INTO AI ANSWER
    # ======================================

    final_response = llm.invoke(
        f"""
You are an AI HR Assistant.

Employee question:
{message}

Information retrieved from the HR system:
{result}

Answer the employee using ONLY the information
provided by the HR system.

Do not invent information.

Give a short, natural and friendly answer.

Do not mention:
- Python
- APIs
- databases
- FAISS
- embeddings
- tools
- internal system details
"""
    )

    return final_response.content