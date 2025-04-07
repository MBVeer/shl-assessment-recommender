from flask import Flask, render_template, request, jsonify
from recommendation_engine import RecommendationEngine
import os
import json

app = Flask(__name__)
recommendation_engine = RecommendationEngine()

@app.route('/')
def index():
    # Get available test types and keywords for the UI
    test_types = recommendation_engine.get_test_types()
    keywords = recommendation_engine.get_keywords()
    
    # Convert to JSON strings for JavaScript
    test_types_json = json.dumps(test_types)
    keywords_json = json.dumps(keywords)
    
    return render_template('index.html', 
                          test_types_json=test_types_json, 
                          keywords_json=keywords_json)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    job_description = data.get('job_description', '')
    
    # Get filter parameters
    filters = {}
    
    # Test type filter
    test_types = data.get('test_types', [])
    if test_types:
        filters['test_type'] = test_types
    
    # Remote testing filter
    remote_testing = data.get('remote_testing')
    if remote_testing is not None:
        filters['remote_testing'] = remote_testing
    
    # Adaptive/IRT filter
    adaptive_irt = data.get('adaptive_irt')
    if adaptive_irt is not None:
        filters['adaptive_irt'] = adaptive_irt
    
    # Max duration filter (in minutes)
    max_duration = data.get('max_duration')
    if max_duration:
        filters['max_duration'] = max_duration
    
    # Get recommendations with filters
    recommendations = recommendation_engine.get_recommendations(
        job_description=job_description,
        k=10,
        filters=filters if filters else None
    )
    
    return jsonify({'recommendations': recommendations})

@app.route('/api/test-types', methods=['GET'])
def get_test_types():
    """API endpoint to get all available test types"""
    test_types = recommendation_engine.get_test_types()
    return jsonify({'test_types': test_types})

@app.route('/api/keywords', methods=['GET'])
def get_keywords():
    """API endpoint to get common keywords from assessments"""
    keywords = recommendation_engine.get_keywords()
    return jsonify({'keywords': keywords})

if __name__ == '__main__':
    app.run(debug=True)