import streamlit as st
from openai import OpenAI
import os

GROQ_API_KEY="your api key"

client=OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

st.set_page_config(page_title="Goal based Customer Support Assistant",layout="centered")
st.title("Customer Support Assistant")
st.markdown("Describe your query.The AI will reply to your questions")

if "chat_history" not in st.session_state:
  st.session_state.chat_history=[]

with st.form("support_form", clear_on_submit=False):
    user_input = st.text_area("Describe what support you need or the issue you're facing", key="input")
    submitted = st.form_submit_button("Submit")

if submitted and user_input.strip() != "":
  st.session_state.chat_history.append({"role":"user","content":user_input})
  with st.spinner("Analysing your queries......"): 
      try:
        messages=[
            {
              "role":"system",
              "content":'''You are a smart and helpful customer support assistant. Your goal is to answer product-related FAQs using internal knowledge. 
                If the user's question is unclear or incomplete, ask polite follow-up questions. 
                Be concise, clear, and structured in your responses.'''
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