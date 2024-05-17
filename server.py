from fastapi import FastAPI, Path, File, UploadFile
from langserve import add_routes
import os
import uvicorn
import openai
from openai import OpenAI
import random
from client import chat_history, store_message, prescription_analysis, openai_llm
from pymongo import MongoClient, ASCENDING
from io import BytesIO
from PIL import Image
from datetime import datetime


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
    query = (f"Generate a medical report of this format."
             f"=================================================="
             f"                 Medical Report"
             f"    =================================================="
             f"    Patient ID: {name}  \n" 
             f"    Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
             f"    --------------------------------------------------"
             f"    Chat History:"
             f"    --------------------------------------------------"
             f"    Chat Summary:"
             f"    --------------------------------------------------"
             f" Return in a separate box containing just "
             f"report which can be printed: {user_history}")
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


# Voice Assistance
@app.get("/voice-assistance")
def process_audio(input_file):
    OPENAI_API_KEY = "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"
    client = OpenAI(api_key=OPENAI_API_KEY)
    audio_file = open(input_file, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file)
    transcribed_text = transcription.text
    query = f"Extract medical information from {transcribed_text} and generate a prescription based on the following doctor-patient conversation:"
    'Patient: Describe patient symptoms and concerns here.'
    "Doctor: Provide doctor's responses, questions asked, and medical advice given to the patient."
    "Patient: Any additional information or responses from the patient."
    "AI Model Task:"
    "Extract Medical Information:"
    "Identify and extract the patient's symptoms, concerns, and any other relevant medical information mentioned in the conversation."
    "Identify and extract the doctor's questions, responses, and medical advice given to the patient."
    "Generate Prescription:"
    "Based on the extracted medical information, generate a prescription for the patient."
    "The prescription should include recommended medications, dosage, frequency, and any additional instructions or precautions."
    "Example Input:"
    "Patient: 'I've been experiencing chest pain and shortness of breath for the past week.'"
    "Doctor: 'When did the symptoms start? Have you experienced any fever or cough? Any history of heart problems or respiratory issues?'"
    "Patient: 'The symptoms started a week ago. No fever or cough. No history of heart problems, but I have asthma.'"
    "Expected Output:"
    "Medical Information Extracted:"
    "Patient Symptoms: Chest pain, shortness of breath"
    "Patient History: Asthma"
    "Doctor's Questions: Onset of symptoms, presence of fever or cough, history of heart problems or respiratory issues"
    "Prescription:"
    "Medication: [List of prescribed medications]"
    "Dosage: [Dosage instructions]"
    "Frequency: [Frequency of medication intake]"
    "Additional Instructions: [Any specific instructions or precautions]"
    "Instructions for AI Model:"
    "Use the provided conversation as input to extract medical information and generate a prescription."
    "Ensure that the prescription is appropriate based on the patient's symptoms, medical history, and any other relevant factors."
    "Provide clear and concise output, including the extracted medical information and the generated prescription."""
    response = openai_llm.invoke(query)
    return response.content



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
