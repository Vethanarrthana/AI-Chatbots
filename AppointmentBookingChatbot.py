import streamlit as st
from openai import OpenAI
import os

GROQ_API_KEY="your api key"

client=OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

st.set_page_config(page_title="Goal based Appointment Booking Assistant",layout="centered")
st.title("Booking Appointment Assistant")
st.markdown("Describe what type of appointment you want to book, reschedule, or cancel.The AI will guide you based on your request.")

if "chat_history" not in st.session_state:
  st.session_state.chat_history=[]

with st.form("support_form", clear_on_submit=False):
    user_input = st.text_area("Describe what type of appointment you want to book, reschedule, or cancel", key="input")
    submitted = st.form_submit_button("Submit")

if submitted and user_input.strip() != "":
  st.session_state.chat_history.append({"role":"user","content":user_input})
  with st.spinner("Analysing your request......"):
      try:
        messages=[
            {
              "role":"system",
              "content":'''You are an intelligent appointment booking assistant.
                Your job is to:
                1. Understand the user's request to book, reschedule, or cancel an appointment.
                2. Collect all necessary details:
                - Full name
                - Purpose of appointment (e.g., doctor visit, consultation)
                - Preferred date and time
                - Alternative date/time if the first is unavailable
                - Contact information (phone or email)
                3. Respond politely, clearly, and in a structured format.
                4. If any required information is missing, ask follow-up questions.
                5. Confirm the appointment once all details are collected.
                6. If needed, politely explain unavailability or suggest alternatives.

                Be concise, professional.Ask follow-up questions.Be clear and structured in response.'''
        }
        ]+st.session_state.chat_history

        response=client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            temperature=0.5,
            max_tokens=800
        )
        ai_reply=response.choices[0].message.content
        st.session_state.chat_history.append({"role":"assistant","content":ai_reply})

        st.success("Recommendation: ")
        st.markdown(ai_reply)

      except Exception as e:
        st.error(f"Error:{str(e)}")