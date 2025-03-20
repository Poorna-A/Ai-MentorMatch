from resume_parser import extract_resume_text
from chatbot import extract_details_from_resume, chat_completion
from utils import find_missing_details
from storage import store_data
import json

def main():

    file_path = input("Enter the path of your resume (PDF/DOCX):")

    resume_text = extract_resume_text(file_path)

    print("resume_text\n",resume_text)

    extracted_data = extract_details_from_resume(resume_text)
    print("extracted_data\n", extracted_data)



    print("\n The extracted data from resume\t")
    print(json.dumps(extracted_data, indent = 4))


    missing_details = find_missing_details(extracted_data)

    if missing_details:
        print("\nThere are some missing details: {missing_details}")
        additional_data = chat_completion(missing_details)
        extracted_data.update(additional_data)

    store_data(extracted_data)
    
    print("\n📄 Extracted Data:")
    print(json.dumps(extracted_data, indent=4))


if __name__ == "__main__":
    main()