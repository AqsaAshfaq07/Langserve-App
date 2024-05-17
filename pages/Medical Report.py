import streamlit as st
from server import generate_report  # assuming backend_file.py contains the generate_report() function

st.title("PrescribeAI")
st.subheader("Get Personalized Medical Reports of Your Data!")

# Get patient's name from user input
patient_name = st.text_input("Enter patient's name:")

# Button to generate medical report
if st.button("Generate Medical Report"):
    if patient_name:
        # Call the backend function to generate report
        report = generate_report(patient_name)
        st.write(report)
        # Output the URL to the browser console
        st.write(f"View the report at http://localhost:8000/report/{patient_name}")
    else:
        st.warning("Please enter a valid patient's name.")
