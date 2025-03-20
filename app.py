import streamlit as st
import json
import io
from resume_parser import extract_resume_text
from chatbot import extract_details_from_resume
from storage import store_data
from utils import find_missing_details

# Initialize session state variables
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = {}
if 'missing_details' not in st.session_state:
    st.session_state.missing_details = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'resume_processed' not in st.session_state:
    st.session_state.resume_processed = False

# Title
st.set_page_config(page_title="AI Resume Chatbot", layout="wide")
st.title("🤖 AI Resume Chatbot")

# File Upload Section
uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF/DOCX)", type=["pdf", "docx"])

# Step 1: Extract Resume Data
if uploaded_file and not st.session_state.resume_processed:
    with st.spinner("Processing your resume..."):
        file_bytes = uploaded_file.read()
        file_buffer = io.BytesIO(file_bytes)

        # Extract text from the resume
        resume_text = extract_resume_text(file_buffer, uploaded_file.type)
        st.session_state.extracted_data = extract_details_from_resume(resume_text)

        # Find missing details
        st.session_state.missing_details = find_missing_details(st.session_state.extracted_data)
        st.session_state.resume_processed = True

        # Debugging: Show missing details at start
        st.write("🔍 Debug - Initial Missing Details:", st.session_state.missing_details)

        # Start chatbot conversation if missing details exist
        if st.session_state.missing_details:
            st.session_state.current_question = st.session_state.missing_details[0]
            st.session_state.chat_history.append(("🤖 Chatbot", f"Can you please provide your {st.session_state.current_question}?"))
        else:
            st.session_state.current_question = None
            st.success("✅ No missing details, profile is complete!")

# Step 2: Display Chat History
for speaker, message in st.session_state.chat_history:
    with st.chat_message("assistant" if speaker == "🤖 Chatbot" else "user"):
        st.markdown(message)

# Step 3: User Input Processing (Only if Profile is Not Complete)
if st.session_state.missing_details:
    user_input = st.chat_input("Type your response here...")

    if user_input:
        # Save user response in chat history
        st.session_state.chat_history.append(("👤 You", user_input))
        
        # Save the response in extracted data
        st.session_state.extracted_data[st.session_state.current_question] = user_input

        # Debugging: Before removing the question
        st.write("🔍 Debug - Before Removing Question:", st.session_state.missing_details)

        # Remove answered question from missing details
        st.session_state.missing_details.pop(0)

        # Debugging: After removing the question
        st.write("🔍 Debug - After Removing Question:", st.session_state.missing_details)

        # Determine next question if any
        if st.session_state.missing_details:
            st.session_state.current_question = st.session_state.missing_details[0]
            st.session_state.chat_history.append(("🤖 Chatbot", f"Can you please provide your {st.session_state.current_question}?"))

            # Debugging: Show updated missing details and current question
            st.write("🔍 Debug - Next Question Selected:", st.session_state.current_question)
            st.write("🔍 Debug - Remaining Missing Details:", st.session_state.missing_details)
        else:
            st.session_state.current_question = None
            st.session_state.chat_history.append(("🤖 Chatbot", "✅ Your profile is now complete! Thank you for providing all the details."))
            store_data(st.session_state.extracted_data)
            st.rerun()  # Force a rerun to update the UI

# Step 4: Display Extracted Resume Data
if st.session_state.extracted_data:
    st.subheader("✅ Extracted Resume Data")
    st.json(st.session_state.extracted_data)

    if not st.session_state.missing_details:
        st.success("✅ Your profile is now complete!")
        st.chat_input("Profile completed! No further input needed.", disabled=True)