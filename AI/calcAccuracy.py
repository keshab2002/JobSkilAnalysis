import pandas as pd
import spacy
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score

nlp = spacy.load('en_core_web_md')

df = pd.read_csv('AI\skillsSplitData1.csv')

df.fillna('', inplace=True)

df['All_Skills'] = df[df.columns[df.columns.str.startswith('Skill')]].values.tolist()
df['All_Skills'] = df['All_Skills'].apply(lambda x: [skill.lower() for skill in x if skill])



job_title_vectors = {}

for job_title, skills in zip(df['Job Title'], df['All_Skills']):
    skill_vectors = [nlp(skill).vector for skill in skills if nlp(skill).has_vector]
    if skill_vectors:
        job_title_vectors[job_title] = np.mean(skill_vectors, axis=0)

with open('job_title_vectors.pkl', 'wb') as f:
    pickle.dump(job_title_vectors, f)





with open('job_title_vectors.pkl', 'rb') as f:
    job_title_vectors = pickle.load(f)

def predict_job_title(skills):
    skill_vectors = [nlp(skill).vector for skill in skills if nlp(skill).has_vector]
    if not skill_vectors:
        return None
    
    input_vector = np.mean(skill_vectors, axis=0).reshape(1, -1)
    
    # Compute cosine similarity between the input vector and all job title vectors
    similarities = {}
    for job_title, vector in job_title_vectors.items():
        similarity = cosine_similarity(input_vector, vector.reshape(1, -1))
        similarities[job_title] = similarity[0][0]
    
    # Return the job title with the highest similarity
    return max(similarities, key=similarities.get)

# Predict job titles for the entire dataset
df['Predicted_Job_Title'] = df['All_Skills'].apply(predict_job_title)

# Calculate the accuracy by comparing the actual job titles with the predicted ones
accuracy = accuracy_score(df['Job Title'], df['Predicted_Job_Title'])

print(f"Model Accuracy: {accuracy * 100:.2f}%")
