
def find_missing_details(extracted_data):
    required_files = {
        "Full Name",
        "Email",
        "Phone Number",
        "Location",
        "Willing to Relocate",
        "Total Experience",
        "Current Job Title",
        "Company History",
        "Job Responsibilities",
        "Industry Experience",
        "Work Preferences",
        "Highest Qualification",
        "University/Institute",
        "Certifications",
        "Skills Acquired During Education",
        "Technical Skills",
        "Soft Skills",
        "Tools & Technologies",
        "Skill Proficiency",
        "Current Salary",
        "Expected Salary",
        "Notice Period",
        "Employment Type",
        "Work Authorization",
        "Preferred Work Type",
        "Personality Traits",
        "Workplace Preferences",
        "Team vs. Individual Work Style",
        "LinkedIn Profile",
        "GitHub, Kaggle, Portfolio",
        "Published Papers, Blogs, Patents"
    }

    missing_details = [field for field in required_files if field not in extracted_data or not extracted_data[field]]

    return missing_details
