from flask import Flask, render_template, request, jsonify
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

class RecommendationEngine:
    def __init__(self, data_file='data/assessments.json'):
        with open(data_file, 'r') as f:
            self.assessments = json.load(f)
        
        # Create assessment descriptions
        self.descriptions = []
        for assessment in self.assessments:
            desc = f"{assessment['name']} {' '.join(assessment['test_type'])} {assessment.get('description', '')}"
            self.descriptions.append(desc)
        
        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.descriptions)
    
    def get_recommendations(self, job_description, k=10):
        # Transform job description
        job_vector = self.vectorizer.transform([job_description])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(job_vector, self.tfidf_matrix).flatten()
        
        # Get top k recommendations
        top_indices = similarity_scores.argsort()[-k:][::-1]
        
        recommendations = []
        for idx in top_indices:
            assessment = self.assessments[idx]
            recommendations.append({
                'name': assessment['name'],
                'url': assessment['url'],
                'remote_testing': assessment['remote_testing'],
                'adaptive_irt': assessment['adaptive_irt'],
                'duration': assessment['duration'],
                'test_type': assessment['test_type'],
                'score': float(similarity_scores[idx])
            })
        
        return recommendations

# Initialize recommendation engine
recommendation_engine = RecommendationEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        job_description = data.get('job_description', '')
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
            
        # Get recommendations
        recommendations = recommendation_engine.get_recommendations(job_description)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 