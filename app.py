
import streamlit as slt
import google.generativeai as genai
import os

# Streamlit app title
slt.title("Gemini-Like Chatbot")

# Configure Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY") or slt.secrets.get("GEMINI_API_KEY", None)

if not gemini_api_key:
    slt.error("API Key is missing! Please set GEMINI_API_KEY in secrets or environment variables.")
else:
    genai.configure(api_key=gemini_api_key)


if "messages" not in slt.session_state:
    slt.session_state.messages = []

if "gemini_model" not in slt.session_state:
    slt.session_state["gemini_model"] = "gemini-1.5-flash"

# Display chat history
for message in slt.session_state.messages:
    with slt.chat_message(message["role"]):
        slt.markdown(message["content"])

# Chat input
if prompt := slt.chat_input("Ask Gemini..."):
    slt.session_state.messages.append({"role": "user", "content": prompt})
    slt.chat_message("user").markdown(prompt)

    with slt.chat_message("assistant"):
        message_placeholder = slt.empty()
        full_response = ""

        try:
            # Initialize the model
            model = genai.GenerativeModel(slt.session_state["gemini_model"])
            chat = model.start_chat(history=[])

            # Retrieve chat history and simulate conversation
            for msg in slt.session_state.messages:
                if msg["role"] == "user":
                    chat.send_message(msg["content"])

            response = chat.send_message(prompt)
            full_response = response.text

            message_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"Error: {e}"
            message_placeholder.markdown(full_response)

        slt.session_state.messages.append({"role": "assistant", "content": full_response})
