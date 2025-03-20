import pandas as pd
import spacy
import pickle

# Load spaCy model for word embeddings
nlp = spacy.load("en_core_web_md")

# Load the dataset
file_path = 'job.csv'
df = pd.read_csv(file_path)

# Function to generate embeddings for job titles and save them in a pickle file
def create_embeddings(df, output_file="job_embeddings.pkl"):
    job_embeddings = []
    
    for index, row in df.iterrows():
        job_title = row['JobTitle']
        job_title_vec = nlp(job_title)  # Get vector for job title
        job_data = {
            'JobTitle': job_title,
            'JobTitle_Link': row['JobTitle_Link'],
            'Company': row['Company'],
            'Location': row['Location'],
            'Criteria': row['Criteria'],
            'Embedding': job_title_vec.vector
        }
        job_embeddings.append(job_data)
    
    # Save the embeddings as a pickle file
    with open(output_file, 'wb') as f:
        pickle.dump(job_embeddings, f)

# Generate the embeddings and save to a file
create_embeddings(df, output_file="job_embeddings.pkl")
print("Job embeddings have been successfully created and saved.")
