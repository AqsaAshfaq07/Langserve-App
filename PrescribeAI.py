import streamlit as st

# Page title
st.title("PrescribeAI   ")

# Define services
services = [
    {
        "name": "Prescription Analysis",
        "image": "Images/prescription-analysis.png"
    },
    {
        "name": "Medical Reports",
        "image": "Images/reports.png"
    },
    {
        "name": "GPT4",
        "image": "Images/gpt4.jpg"
    },
    {
        "name": "Chat History",
        "image": "Images/history.png"
    }
]

# Divide services into two columns
col1, col2 = st.columns(2)

for i in range(len(services)):
    if i < len(services)//2:
        with col1:
            st.write(f"### {services[i]['name']}")
            st.image(services[i]['image'], width=250, )

    else:
        with col2:
            st.write(f"### {services[i]['name']}")
            st.image(services[i]['image'], width=250)



