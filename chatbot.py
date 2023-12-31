import streamlit as st
import base64

import google.generativeai as genai

with st.sidebar:
    gemini_api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
    "[Get a Gemini API key](https://ai.google.dev/tutorials/setup)"

st.markdown("<h1 style='font-size: 2em;'>Gemini AI</h1>", unsafe_allow_html=True)
st.caption("A Chatbot powered by Gemini LLM")

avatars={"user":"user.jpeg","Gemini":"Gemini.jpg"}

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "Gemini", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"],avatar = avatars[msg["role"]]).write(msg["content"])

if prompt := st.chat_input():
    if not gemini_api_key:
        st.info("Please add your API key to continue.")
        st.stop()

    genai.configure(api_key=gemini_api_key)

    #Loading the gemini model
    model = genai.GenerativeModel('gemini-pro')

    st.session_state.messages.append({"role": "user", "content": prompt})

    # st.chat_message("user").write(prompt)
    st.chat_message("user", avatar="user.jpeg").write(prompt)

    with st.spinner("Waiting for Gemini to generate a response..."):
        response = model.generate_content(prompt)

    st.session_state.messages.append({"role": "Gemini", "content": response.text})
    st.chat_message("Gemini",avatar = "Gemini.jpg").write(response.text)