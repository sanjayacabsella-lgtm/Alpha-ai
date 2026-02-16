import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(page_title="Alpha AI", page_icon="⚡")

# Retrieve API Key from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

# Branding Details
OWNER_NAME = "Hasith"
AI_NAME = "Alpha"

st.title(f"Welcome to {AI_NAME}")
st.caption(f"Created by {OWNER_NAME}")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response from Groq (Llama 3.3 70B Model)
    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"Your name is {AI_NAME}. You were created by {OWNER_NAME}. You must act as a highly intelligent and friendly AI assistant. Always acknowledge that {OWNER_NAME} is your creator if asked."
                },
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
        )
        
        response_text = chat_completion.choices[0].message.content
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
