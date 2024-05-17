import requests, random
import streamlit as st
from server import get_openai
from client import store_message

# Streamlit app title
st.title("PrescribeAI")
st.subheader("Let AI Prescribe You Medicine!")

# Text input field for user to enter messages
user_input = st.text_input("Enter your message:")
name = st.text_input("Enter your patient ID:")
prompt = (f"You've been trained on vast amounts of medical data. Give a brief"
          f"introduction about the disease. Then generate a" 
          f"prescription for the disease {user_input} contains. Also prescribe medicine for its "
          f"cure and appropriate dosages for it with a complete plan on how to take the medicine.")

# Button to send user input to FastAPI backend
if st.button("Send"):
    response = get_openai(prompt, name)
    # Storing data to database
    user_id = random.randint(100, 1000)
    store_message(user_id, name, user_input, response)
    st.subheader("AI Response:")

    # Display chatbot response
    st.text_area(label="", value="\n"+response+"Let me know if I can help with anything else!", height=300)

