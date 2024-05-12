from fastapi import FastAPI, Path, File, UploadFile
from langserve import add_routes
import os
import uvicorn
import openai
import random
from client import chat_history, store_message, prescription_analysis, openai_llm
from pymongo import MongoClient, ASCENDING
from io import BytesIO
from PIL import Image


openai_api_key = "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"

app = FastAPI(
    title="Langserve App",
    version="1.0.0",
    description="A simple API server"
)

# Default Route
@app.get("/")
def home():
    return "WELCOME TO PRESCRIBEAI :)"


# Question Answering with ChatGPT
@app.get("/openai/{prompt}/{name}")
def get_openai(prompt, name):
    response = openai_llm.invoke(prompt)
    user_id = str(random.randint(100, 1000))
    store_message(user_id, name, prompt, response.content)
    return response.content


# Patient Chat History Retrieval
@app.get("/get-patient/{name}")
def get_chat_history(name):
    """ Retrieves a user's chat history, sorted by timestamp. """
    messages = list(chat_history.find({"user_name": name}).sort("timestamp", ASCENDING))
    formatted_history = []
    for message in messages:
        user_message = f"User: {message['User']}"
        ai_message = f"AI : {message['AI']}"
        formatted_history.append(user_message)
        formatted_history.append(ai_message)
    return  "\n".join(formatted_history)


# Getting Custom Report for a Conversation
@app.get("/report/{name}")
def generate_report(name):
    user_history = get_chat_history(name)
    query = f"Generate a summary of this conversation: {user_history}"
    report = openai_llm.invoke(query)
    return report.content


# Prescription Analysis
@app.get("/prescription")
def get_prescription(image_file):
    image = Image.open(BytesIO(image_file.read()))
    extracted_text = prescription_analysis(image)
    prompt = (f"You're a health care professional and you've been trained on "
              f"vast amounts of medical data. Looking at this prescription, provide "
              f"more information about this prescription. {extracted_text}")
    info = openai_llm.invoke(prompt)
    prescription = info.content
    return prescription


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)