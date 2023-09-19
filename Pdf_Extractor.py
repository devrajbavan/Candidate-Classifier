import os
import csv
import fitz  # PyMuPDF

def extract_section_info(section_text):
    # Split the section text into lines
    lines = section_text.split("\n")
    
    # Initialize variables for different sections
    language = "Not Found"
    hobby = "Not Found"
    skills = "Not Found"
    education = "Not Found"
    
    # Define flags to identify which section is being parsed
    parsing_language = False
    parsing_hobby = False
    parsing_skills = False
    parsing_education = False
    
    # Iterate through lines and identify section content
    for line in lines:
        if "Language" in line:
            parsing_language = True
            parsing_hobby = False
            parsing_skills = False
            parsing_education = False
        elif "Hobby" in line:
            parsing_language = False
            parsing_hobby = True
            parsing_skills = False
            parsing_education = False
        elif "Skills" in line:
            parsing_language = False
            parsing_hobby = False
            parsing_skills = True
            parsing_education = False
        elif "Education" in line:
            parsing_language = False
            parsing_hobby = False
            parsing_skills = False
            parsing_education = True
        elif parsing_language:
            language = line.strip()
        elif parsing_hobby:
            if line.strip() != "":
                hobby = line.strip()
        elif parsing_skills:
            if line.strip() != "":
                skills = line.strip()
        elif parsing_education:
            if line.strip() != "":
                if education == "Not Found":
                    education = line.strip()
                else:
                    education += "\n" + line.strip()
    
    return language, hobby, skills, education

def extract_resume_info(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Initialize variables to store resume information
    category = "Not Found"
    section_text = ""
    
    # Loop through each page in the PDF
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        page_text = page.get_text()
        
        # Check for keywords to identify resume sections
        if "Summary" in page_text:
            category = "Summary"
        elif "Experience" in page_text:
            category = "Experience"
        elif "Education" in page_text:
            category = "Education"
        
        # Extract section text based on keywords
        if category != "Not Found":
            section_text += page_text + "\n"
    
    # Close the PDF document
    pdf_document.close()
    
    # Extract detailed information from each section
    language, hobby, skills, education = extract_section_info(section_text)
    
    # Return the extracted information
    return {
        "Category": category,
        "Language": language,
        "Hobby": hobby,
        "Skills": skills,
        "Education": education
    }

# Directory containing the PDF resumes
directory_path = '/home/cdac/Documents/Devraj/Assesment/Resume_dataset/data/data/INFORMATION-TECHNOLOGY/12635195.pdf'

# Initialize a list to store extracted data
all_resume_data = []

# Iterate through all files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.pdf'):
        # Construct the full path to the PDF file
        pdf_path = os.path.join(directory_path, filename)
        
        # Extract resume information from the PDF file
        resume_info = extract_resume_info(pdf_path)
        
        # Include the file name in the dictionary
        resume_info["File"] = filename
        
        # Append the extracted information to the list
        all_resume_data.append(resume_info)

# Define the path for the output CSV file
output_csv_path = 'Resume_data_4.csv'

# Define the CSV header
header = ["File", "Category", "Language", "Hobby", "Skills", "Education"]

# Write the extracted data to the CSV file
with open(output_csv_path, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=header)
    
    # Write the header row
    writer.writeheader()
    
    # Write each row of data
    for resume_info in all_resume_data:
        writer.writerow({
            "File": resume_info["File"],
            "Category": resume_info["Category"],
            "Language": resume_info["Language"],
            "Hobby": resume_info["Hobby"],
            "Skills": resume_info["Skills"],
            "Education": resume_info["Education"]
        })

print(f"Data has been saved to {output_csv_path}")

