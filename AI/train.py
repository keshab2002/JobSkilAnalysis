import pandas as pd
import spacy
import numpy as np
import pickle  

nlp = spacy.load('en_core_web_md')

df = pd.read_csv('skillsSplitData.csv')

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

print("Training complete and job title vectors saved.")
