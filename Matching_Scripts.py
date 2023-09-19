import os
import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Directory containing CVs in PDF format
root_directory = "/home/cdac/Documents/Devraj/resume"

# Define the job description as a string
job_description = '''{
    'company_name': 'Google',
    'job_description': 'minimum qualifications\nbachelors degree or equivalent practical experience years of experience in saas or productivity tools businessexperience managing enterprise accounts with sales cycles\npreferred qualifications\n years of experience building strategic business partnerships with enterprise customersability to work through and with a reseller ecosystem to scale the businessability to plan pitch and execute a territory business strategyability to build relationships and to deliver results in a crossfunctionalmatrixed environmentability to identify crosspromoting and uppromoting opportunities within the existing account baseexcellent account management writtenverbal communication strategic and analyticalthinking skills\nabout the job\nas a member of the google cloud team you inspire leading companies schools and government agencies to work smarter with google tools like google workspace search and chrome you advocate the innovative power of our products to make organizations more productive collaborative and mobile your guiding light is doing whats right for the customer you will meet customers exactly where they are at and provide them the best solutions for innovation using your passion for google products you help spread the magic of google to organizations around the world\nthe google workspace team helps customers transform and evolve their business through the use of googles productivity collaboration and content management suite of applications as part of an entrepreneurial team in this growing business you will help shape the future of businesses use technology to connect with customers employees and partners\nas a google workspace sales specialist you will be responsible for maintenance and expansion of google workspace business growth across the region with customers in this role youll create and execute the strategy and provide unique insights on applying google workspace solutions to enterprisesyou will build an excellent pipeline and work with the account teams to build out the customer solution and establish partnerships you will strategize with partners to increase account and territory business growth you will work directly with customers coordinate internal resources and construct successful strategies at account and territory level\ngoogle cloud accelerates organizations ability to digitally transform their business with the best infrastructure platform industry solutions and expertise we deliver enterprisegrade solutions that leverage googles cuttingedge technology  all on the cleanest cloud in the industry customers in more than  countries and territories turn to google cloud as their trusted partner to enable growth and solve their most critical business problems',
    'position_title': 'Sales Specialist',
    'description_length': 2727,
    'model_response': ' {\n  "Core Responsibilities": "Responsible for expanding Google Workspace product adoption across an assigned territory. Build relationships with customers to understand needs and provide Google Workspace solutions. Partner with account teams to construct solutions and grow business for Google Workspace.",\n  "Required Skills": "Bachelor\'s degree or equivalent experience. Experience managing enterprise SaaS accounts and sales cycles.", \n  "Educational Requirements": "Bachelor\'s degree or equivalent experience.",\n  "Experience Level": "Experience managing enterprise SaaS accounts and sales cycles.",\n  "Preferred Qualifications": "Experience building strategic partnerships with enterprise customers. Ability to work through a reseller ecosystem. Excellent communication and strategic thinking skills.",\n  "Compensation and Benefits": "N/A"\n}'
}
'''

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    cv_text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    for page in pdf_reader.pages:
        cv_text += page.extract_text()
    return cv_text

# Initialize a list to store candidates and their similarity scores
candidate_scores = []

# Iterate through all subdirectories and CVs
for root, subdirectories, files in os.walk(root_directory):
    for filename in files:
        if filename.endswith(".pdf"):  # Check if it's a PDF file
            cv_path = os.path.join(root, filename)
            cv_text = extract_text_from_pdf(cv_path)

            # Calculate cosine similarity as you did in your original script
            documents = [cv_text, job_description]
            vectorizer = CountVectorizer().fit_transform(documents)
            cosine_matrix = cosine_similarity(vectorizer)
            similarity_percentage = cosine_matrix[0][1] * 100
            similarity_percentage = round(similarity_percentage, 2)

            # Store the candidate filename and similarity score
            candidate_scores.append((filename, similarity_percentage))

# Sort candidates by similarity score in descending order
candidate_scores.sort(key=lambda x: x[1], reverse=True)

# Print the top 5 candidates
print("Top 5 Candidates:")
for i, (filename, similarity) in enumerate(candidate_scores[:5], start=1):
    print(f"{i}. {filename} - Similarity: {similarity}%")
