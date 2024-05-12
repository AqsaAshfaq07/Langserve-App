import requests
import streamlit as st
from app import get_chat_history


st.title("PrescribeAI")
st.subheader("Never Lose Your Medical Conversations!")

# Text input field for user to enter the name
name = st.text_input("Enter the name:")

# Button to fetch chat history
if st.button("Fetch Chat History"):
    # history =

    # Display chat history
    chat_history = get_chat_history(name)
    st.subheader("Chat History")
    st.text_area(label="", value=chat_history, height=300)
