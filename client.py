# Installing necessary libraries for Connection with MongoDB
import pymongo, random
from pymongo import MongoClient, ASCENDING
from datetime import datetime
from PIL import Image
import requests, openai, cv2, pytesseract
from openai import OpenAI
from langchain_community.chat_models import ChatOpenAI


openai_llm = ChatOpenAI(openai_api_key="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")


# DATABASE CONNECTION
CONNECTION_STRING = "mongodb+srv://ashfaqaqsa883:RQavPYfFiqkAmlkL@cluster0.whmef7a.mongodb.net/"
client = MongoClient(CONNECTION_STRING)
db = client["sample_mflix"]  # This should match the database name in your connection string
collection = db['users']
chat_history = db.chat_history
chat_history.create_index([("user_id", ASCENDING), ("timestamp", ASCENDING)])


def store_message(user_id, name, message, response_data):
    """Stores a message in the database."""
    chat_history.insert_one({
        "user_id": user_id,
        "user_name": name,
        "timestamp": datetime.utcnow(),
        "User": message,
        "AI": response_data
    })


# PRESCRIPTION ANALYSIS
def prescription_analysis(image):
    text = pytesseract.image_to_string(image)
    extracted_text = text
    return extracted_text
