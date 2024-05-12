import requests
import streamlit as st
from PIL import Image
import time
from app import get_prescription

st.set_page_config(layout="wide")  # in streamlit app, the layout default setting is 'centered'
STYLES = {
    "GPT-4": "candy",
    "GPT-3.5 Turbo ": "composition_vii",
}


st.title("PrescribeAI")
st.subheader("Get Information About Your Prescription!")
image = st.file_uploader("Choose an image")
style = st.selectbox("Choose the Model", [i for i in STYLES.keys()])

if st.button("Start Analysis"):
    start_time = time.time()
    if image is not None:
        files = {"image_file": image}
        res = get_prescription(image)
        st.image(image)
        st.subheader("Generated Prescription:")
        st.write(res)
        # else:
        #     st.write("Error generating prescription. Please try again.")
    end_time = time.time()
    st.text(f'Total Run Time :{end_time - start_time}s')
