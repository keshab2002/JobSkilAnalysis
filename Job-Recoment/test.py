import spacy
import pickle
import numpy as np

# Load spaCy model for word embeddings
nlp = spacy.load("en_core_web_md")

# Function to calculate cosine similarity between two vectors
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

# Function to find the top N jobs similar to the input job domain
def find_top_jobs(job_domain, embedding_file="job_embeddings.pkl", n=5):
    # Load the precomputed job embeddings from the pickle file
    with open(embedding_file, 'rb') as f:
        job_embeddings = pickle.load(f)
    
    # Convert the input job domain into a vector
    job_domain_vec = nlp(job_domain).vector
    
    # Calculate similarity between the input job domain and the job embeddings
    similarities = []
    
    for job_data in job_embeddings:
        # Compute cosine similarity
        similarity_score = cosine_similarity(job_domain_vec, job_data['Embedding'])
        similarities.append((similarity_score, job_data))
    
    # Sort the jobs by similarity score in descending order
    similarities = sorted(similarities, key=lambda x: x[0], reverse=True)
    
    # Return the top N most similar jobs
    return similarities[:n]

# Get user input for job domain
input_job_domain = "Software Engineer"

# Find the top 5 jobs
top_jobs = find_top_jobs(input_job_domain, embedding_file="job_embeddings.pkl", n=5)

# Display the top jobs
for i, (score, job) in enumerate(top_jobs, 1):
    print(f"Rank {i}:")
    print(f"Job Title: {job['JobTitle']}")
    print(f"Company: {job['Company']}")
    print(f"Location: {job['Location']}")
    print(f"Criteria: {job['Criteria']}")
    print(f"Job Link: {job['JobTitle_Link']}")
    print(f"Similarity Score: {score:.4f}")
    print("-" * 80)
