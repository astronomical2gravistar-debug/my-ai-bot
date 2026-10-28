import streamlit as st
from google import genai

# Set up the web page title and icon
st.set_page_config(page_title="My AI Assistant", page_icon="🤖")
st.title("🤖 My Personal AI Assistant")

# Replace this with your actual API key from Google AI Studio
# This safely looks for your key in Streamlit secrets, or lets you type it locally for testing
API_KEY = st.secrets.get("GEMINI_API_KEY", "YOUR_LOCAL_API_KEY_HERE")

# Initialize the Gemini client
client = genai.Client(api_key=API_KEY)

# Store chat history in the web session so messages don't disappear
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Create a text box at the bottom for user input
if prompt := st.chat_input("Ask me anything..."):
    # 1. Show the user's message in the chat UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# List of models to try in order
    MODELS_TO_TRY = ["gemini-3.8-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite"]

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text = None
            
            # Loop through available models until one responds
            for model_name in MODELS_TO_TRY:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    response_text = response.text
                    break  # Success! Stop trying other models.
                except Exception:
                    continue  # If this model is busy, automatically try the next one
            
            if response_text:
                st.write(response_text)
            else:
                st.error("All Gemini servers are currently busy. Please try again in a few seconds!")
            
    # 3. Save the bot's response to history
    st.session_state.messages.append({"role": "assistant", "content": response.text})