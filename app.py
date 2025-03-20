from flask import Flask, request, jsonify
import numpy as np
import joblib
from scipy.spatial.distance import cosine
import spacy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the pre-trained job title vectors (stored in the dictionary)
try:
    model1 = joblib.load('model1.pkl')  # First model: dictionary of job title vectors
    print(f"First model loaded successfully: {type(model1)}")
except Exception as e:
    model1 = None
    print(f"Error loading first model: {e}")

try:
    model2 = joblib.load('model2.pkl')  # Second model: list of job details
    print(f"Second model loaded successfully: {type(model2)}")
except Exception as e:
    model2 = None
    print(f"Error loading second model: {e}")

# Load spaCy language model
nlp = spacy.load('en_core_web_md')

def convert_ndarray_to_list(data):
    """ Convert ndarray or nested ndarrays to list """
    if isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, list):
        return [convert_ndarray_to_list(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_ndarray_to_list(value) for key, value in data.items()}
    else:
        return data

@app.route('/')
def home():
    return "Welcome to the Job Recommendation API!"

@app.route('/recommend', methods=['POST'])
def recommend_jobs():
    if model1 is None or model2 is None:
        return jsonify({
            'status': 'error',
            'message': 'One or both models could not be loaded.'
        }), 500

    try:
        user_input = request.get_json()

        # Validate input
        skills = user_input.get('skills')
        if not skills or not isinstance(skills, str):
            return jsonify({
                'status': 'error',
                'message': 'Invalid input. Please provide skills as a comma-separated string.'
            }), 400

        # Process the comma-separated skills string
        skill_list = [skill.strip() for skill in skills.split(',')]
        
        # Get skill vectors using spaCy
        user_skill_vectors = [nlp(skill).vector for skill in skill_list if nlp(skill).has_vector]
        
        if not user_skill_vectors:
            return jsonify({
                'status': 'error',
                'message': 'No valid vectors found for the given skills.'
            }), 400

        # Calculate the average vector for the user's skills
        user_vector = np.mean(user_skill_vectors, axis=0)
        user_vector_list = convert_ndarray_to_list(user_vector)  # Convert ndarray to list

        # Debug print
        print("User vector (converted to list):", user_vector_list)

        # Find the most similar job based on cosine similarity from the first model
        best_match1 = None
        best_similarity1 = float('-inf')

        for job_title, job_vector in model1.items():  # model1 is the dictionary of job vectors
            job_vector_list = convert_ndarray_to_list(job_vector)  # Convert ndarray to list
            similarity = 1 - cosine(user_vector_list, job_vector_list)
            if similarity > best_similarity1:
                best_similarity1 = similarity
                best_match1 = job_title

        if not best_match1:
            return jsonify({
                'status': 'error',
                'message': 'No suitable job found in the first model.'
            }), 400

        # Retrieve detailed job recommendations from the second model
        # Match based on the 'JobTitle' key
        recommendations_from_model2 = [job for job in model2 if job.get('JobTitle') == best_match1]

        if not recommendations_from_model2:
            return jsonify({
                'status': 'error',
                'message': 'No suitable job found in the second model.'
            }), 400

        # Debug print
        print("Recommendations from model2:", recommendations_from_model2)

        # Ensure that all data to be returned is in a serializable format
        response = {
            'status': 'success',
            'first_model_recommendation': best_match1,
            'second_model_recommendations': convert_ndarray_to_list(recommendations_from_model2)
        }
        print("Response data:", response)

        return jsonify(response)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
