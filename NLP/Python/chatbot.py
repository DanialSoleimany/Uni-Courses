import streamlit as st
import google.generativeai as genai

# Set up Streamlit UI
st.title("Chatbot")

# Load API key securely from secrets.toml
if "GEMINI_API_KEY" not in st.secrets:
    st.error("API key missing! Ensure .streamlit/secrets.toml is set up.")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Initialize model in session state
if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = "gemini-1.5-flash"

# Initialize chat history if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat UI
    with st.chat_message("user"):
        st.markdown(prompt)

    # Store user message in chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate AI response using Gemini 1.5 Flash
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # Load Gemini AI model
        model = genai.GenerativeModel(st.session_state["gemini_model"])

        # Pass full conversation history for better responses
        response = model.generate_content([
            {"role": m["role"], "parts": [m["content"]]}
            for m in st.session_state.messages
        ])

        # Display AI response
        full_response = response.text
        message_placeholder.markdown(full_response)

    # Store assistant response in chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})