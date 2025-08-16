# agent_runner.py
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    set_tracing_disabled
)

# Load environment variables
load_dotenv()
set_tracing_disabled(disabled=True)

# Setup Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)

llm_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# Structured schema
class ActionPlan(BaseModel):
    summary: List[str]
    decisions: List[str]
    tasks: List[str]
    next_meeting: Optional[str]

# Create agent
agent = Agent(
    name="Meeting Notes Agent",
    instructions="""
You are an assistant that extracts an Action Plan from meeting transcripts.
Whenever you receive a meeting transcript, extract and return the following structured information:

Summary – What was discussed

Decisions – What was finalized or agreed upon

Tasks – Include task description, assignee, deadline, and priority (if mentioned)

Next Meeting – If a follow-up meeting is mentioned, include the date/time

If any information is vague or missing, leave the corresponding fields empty without making assumptions.
""",
    output_type=ActionPlan,
    model=llm_model
)

# Async runner function for Streamlit
async def run_meeting_agent(transcript: str):
    result = await Runner.run(agent, transcript)
    return {
        "summary": result.final_output.summary,
        "decisions": result.final_output.decisions,
        "tasks": result.final_output.tasks,
        "next_meeting": result.final_output.next_meeting
    }
