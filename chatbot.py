import openai
import json
from config import client


def extract_details_from_resume(resume_text):
    
    prompt= f"""
    You are an AI that extracts structured details from resumes.
    Extract the following details from the given resume text:
    - Full Name
    - Email
    - Phone Number
    - Location (City, State, Country)
    - Willing to Relocate? (Yes/No)
    - Total Experience (in Years)
    - Current Job Title
    - Company History (Employer names and duration)
    - Job Responsibilities
    - Industry Experience
    - Work Preferences
    - Highest Qualification
    - University/Institute
    - Certifications
    - Technical Skills
    - Soft Skills
    - Tools & Technologies
    - LinkedIn Profile
    - GitHub, Kaggle, Portfolio

    Return the response in a structured JSON format. Do not include explanations.

    Resume Text:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="BT-OpenAIGPT4",
        messages=[{"role": "system", "content": "You are an AI that extracts structured data from resumes."},
                  {"role": "user", "content": prompt}]
    )
    try:
        response_text = response.choices[0].message.content.strip()
        cleaned_text = response_text.strip("```json").strip()


        print("\nresponse", cleaned_text)
        print("...................................")
        extracted_data = json.loads(cleaned_text)
        print("\njson formatted data", extracted_data)
        print("...................................")

        return extracted_data


    except json.JSONDecodeError:
        return {"error": "failed to parse the response"}



def chat_completion(missing_details):
    """Collects missing details from the user in a simple and concise manner."""
    user_data = {}
    print("\n🤖 Chatbot: Let's quickly complete your profile!")

    question_templates = {
        "Notice Period": "How long is your notice period?",
        "Willing to Relocate": "Are you open to relocating? (Yes/No)",
        "Workplace Preferences": "Do you have any preferred work location? (Remote/On-site/Hybrid)",
        "Work Authorization": "Do you have valid work authorization? (Yes/No)",
        "Current Salary": "What is your current salary (in LPA or currency)?",
        "Preferred Work Type": "Do you prefer remote, on-site, or hybrid work?",
        "Skill Proficiency": "What technical skills are you most confident in?",
        "Skills Acquired During Education": "What skills did you gain during your education?",
        "Expected Salary": "What is your expected salary (in LPA or currency)?",
        "Team vs. Individual Work Style": "Do you prefer working in a team or individually?",
        "Personality Traits": "How would you describe yourself in one or two words?",
        "Published Papers, Blogs, Patents": "Have you published any papers, blogs, or patents? (Yes/No)",
        "Employment Type": "Are you working full-time, part-time, contract, or freelancing?"
    }

    for detail in missing_details:
        prompt = question_templates.get(detail, f"Please provide your {detail}.")
        
        response = client.chat.completions.create(
            model="BT-OpenAIGPT4",
            messages=[
                {"role": "system", "content": "You are a friendly chatbot collecting missing resume details in a simple way."},
                {"role": "user", "content": prompt}
            ]
        )

        chatbot_question = response.choices[0].message.content.strip()
        user_input = input(f"🤖 Chatbot: {chatbot_question}\n👤 You: ").strip()

        # Clean user input before saving
        cleaned_input = clean_response_with_openai(user_input, detail)
        user_data[detail] = cleaned_input

    return user_data


def clean_response_with_openai(response, field):
    """Uses OpenAI to clean user responses and extract only relevant keywords."""
    
    prompt = f"""
    You are a data processing assistant. Your task is to extract only the relevant keyword(s) from a user's response.
    
    **Field:** {field}
    **User Response:** "{response}"
    
    Extract the clean response in **a concise and structured format**. For:
    - **Yes/No questions**, return "Yes" or "No".
    - **Work preferences**, return one word like "Remote", "On-site", or "Hybrid".
    - **Salary-related responses**, extract only the numeric value.
    - **Skills**, return only the key technologies (comma-separated).
    - **Soft skills**, return a few words summarizing traits.
    - **Education**, return only the highest degree and university.
    
    Return the cleaned response **without any extra text**.
    """

    response = client.chat.completions.create(
        model="BT-OpenAIGPT4",
        messages=[
            {"role": "system", "content": "You are a smart AI that extracts only the necessary keywords from user responses."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


# def chat_completion(missing_details):
#     user_data = {}

#     print("\n🤖 Chatbot: Hi! Let's complete your profile. I will only ask for missing details.")
    
#     for detail in missing_details:
#         prompt = f"Ask the user in a conversational way for their {detail}. Keep it natural and avoid repeating phrases."

#         response = client.chat.completions.create(
#             model="BT-OpenAIGPT4",
#             messages=[{"role": "system", "content": "You are a friendly chatbot collecting missing resume details."},
#                       {"role": "user", "content": prompt}]
#         )

#         chatbot_questions = response.choices[0].message.content.strip()
#         user_input = input(f"🤖 Chatbot: {chatbot_questions}\n👤 You: ")
#         user_data[detail] = user_input

#     return user_data
