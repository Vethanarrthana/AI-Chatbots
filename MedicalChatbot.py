import streamlit as st
from openai import OpenAI
import os

GROQ_API_KEY="your api key"

client=OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

st.set_page_config(page_title="Goal based Medical Triage Assistant",layout="centered")
st.title("Goal based Medical Triage Assistant")
st.markdown("Describe your health condition or symptoms.The AI will decide wheather you need medical assistance or not")

if "chat_history" not in st.session_state:
  st.session_state.chat_history=[]

with st.form("support_form", clear_on_submit=False):
    user_input = st.text_area("Describe your symptoms or how you're feeling", key="input")
    submitted = st.form_submit_button("Submit")

if submitted and user_input.strip() != "":
  st.session_state.chat_history.append({"role":"user","content":user_input})
  with st.spinner("Analysing your condition......"):
      try:
        messages=[
            {
              "role":"system",
             "content":'''You are a goal-based medical assistant.Your goal is to analyze user symptoms and advise one of the following
             1. Rest at home, 2.consult a doctor, 3.Go to clinic,Emergency.Be cautious.Ask follow-up questions.Be clear and structured in response.'''
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