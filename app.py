import streamlit as st
import getpass
import os
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate


if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

st.title("ChatGPT-like clone")

if "conversation" not in st.session_state:
    prompt = PromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.\n\nCurrent conversation:\n{history}\nHuman: {input}\nAI: ")
    llm = OpenAI(temperature=0)
    st.session_state.conversation = prompt | llm

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if input := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.markdown(input)

    with st.chat_message("assistant"):
        stream = st.session_state.conversation.stream(
            {
                "input": input,
                "history": st.session_state.memory.load_memory_variables({})["history"],
            }
        )
        response = st.write_stream(stream)
    st.session_state.memory.save_context({"input": input}, {"output": response})
    st.session_state.messages.append({"role": "assistant", "content": response})