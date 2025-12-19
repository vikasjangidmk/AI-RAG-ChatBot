import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.title("RAG CHATBOT")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

prompt = st.chat_input("Pass your prompt here:")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    system_prompt = ChatPromptTemplate.from_template(
        """You are very smart at everything.
You always give the best, most accurate and precise answers.
Answer the following question directly. No small talk.

Question: {user_prompt}
"""
    )

    # OpenRouter Chat Model
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        model="meta-llama/llama-3-8b-instruct"
        
    )

    chain = system_prompt | llm | StrOutputParser()

    response = chain.invoke({"user_prompt": prompt})

    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
