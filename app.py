# app.py
import streamlit as st
import asyncio
from agent_logic import run_meeting_agent  # 👈 we'll define this function below

st.set_page_config(page_title="Meeting Agent", layout="centered")

st.title("📋 AI Meeting Transcript Analyzer")
st.markdown("Paste your **meeting transcript** below and get a structured summary with Gemini AI.")

transcript_input = st.text_area("✍️ Paste Transcript Here", height=300)

if st.button("🔍 Analyze Transcript"):
    if transcript_input.strip() == "":
        st.warning("Please enter a transcript first.")
    else:
        with st.spinner("Processing with Gemini Agent..."):
            output = asyncio.run(run_meeting_agent(transcript_input))
        
        st.success("✅ Transcript Processed")

        st.subheader("📝 Summary")
        for item in output['summary']:
            st.markdown(f"- {item}")

        st.subheader("🧠 Decisions")
        for decision in output['decisions']:
            st.markdown(f"- {decision}")

        st.subheader("✅ Tasks")
        for task in output['tasks']:
            st.markdown(f"- {task}")

        st.subheader("📅 Next Meeting")
        st.markdown(output['next_meeting'] or "_No next meeting mentioned._")
