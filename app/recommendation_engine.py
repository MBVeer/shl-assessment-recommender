import json
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import Counter

class RecommendationEngine:
    def __init__(self, data_file='data/assessments.json'):
        self.data_file = data_file
        self.assessments = self._load_assessments()
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.assessment_descriptions = self._create_assessment_descriptions()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.assessment_descriptions)
        self.test_types = self._extract_test_types()
        self.keywords = self._extract_keywords()

    def _load_assessments(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading assessments: {e}")
            return []

    def _extract_test_types(self):
        """Extract all unique test types from assessments"""
        test_types = set()
        for assessment in self.assessments:
            test_types.update(assessment['test_type'])
        return sorted(list(test_types))

    def _extract_keywords(self):
        """Extract common keywords from assessment descriptions"""
        all_words = []
        for assessment in self.assessments:
            # Add name words
            all_words.extend(re.findall(r'\w+', assessment['name'].lower()))
            # Add description words
            all_words.extend(re.findall(r'\w+', assessment['description'].lower()))
            # Add test type words
            all_words.extend([t.lower() for t in assessment['test_type']])
        
        # Count word frequencies
        word_counts = Counter(all_words)
        # Filter out common words and short words
        keywords = [word for word, count in word_counts.most_common(50) 
                   if len(word) > 3 and count > 1]
        return keywords

    def _create_assessment_descriptions(self):
        descriptions = []
        for assessment in self.assessments:
            # Create a rich description combining name, test types, and description
            test_types = ' '.join(assessment['test_type'])
            # Add duration as a feature
            duration = assessment['duration'].replace(' minutes', '')
            # Add remote and adaptive features
            features = []
            if assessment['remote_testing']:
                features.append('remote')
            if assessment['adaptive_irt']:
                features.append('adaptive')
            
            description = f"{assessment['name']} {test_types} {assessment['description']} {duration} {' '.join(features)}"
            descriptions.append(description)
        return descriptions

    def get_recommendations(self, job_description, k=10, filters=None):
        """
        Get recommendations based on job description with optional filters
        
        Args:
            job_description (str): The job description to match against
            k (int): Number of recommendations to return
            filters (dict): Optional filters for test_type, remote_testing, adaptive_irt, max_duration
            
        Returns:
            list: List of recommendation dictionaries
        """
        if not self.assessments:
            return []

        # Apply filters if provided
        filtered_assessments = self.assessments
        if filters:
            if 'test_type' in filters and filters['test_type']:
                filtered_assessments = [
                    a for a in filtered_assessments 
                    if any(t in a['test_type'] for t in filters['test_type'])
                ]
            
            if 'remote_testing' in filters and filters['remote_testing'] is not None:
                filtered_assessments = [
                    a for a in filtered_assessments 
                    if a['remote_testing'] == filters['remote_testing']
                ]
            
            if 'adaptive_irt' in filters and filters['adaptive_irt'] is not None:
                filtered_assessments = [
                    a for a in filtered_assessments 
                    if a['adaptive_irt'] == filters['adaptive_irt']
                ]
            
            if 'max_duration' in filters and filters['max_duration']:
                max_minutes = int(filters['max_duration'])
                filtered_assessments = [
                    a for a in filtered_assessments 
                    if int(a['duration'].split()[0]) <= max_minutes
                ]

        # If no assessments match filters, return empty list
        if not filtered_assessments:
            return []

        # Create a mapping from filtered assessments to original indices
        filtered_indices = [i for i, a in enumerate(self.assessments) if a in filtered_assessments]
        
        # Transform the job description
        job_tfidf = self.vectorizer.transform([job_description])
        
        # Calculate similarity scores for filtered assessments
        filtered_scores = cosine_similarity(job_tfidf, self.tfidf_matrix[filtered_indices]).flatten()
        
        # Get top k indices from filtered results
        top_filtered_indices = filtered_scores.argsort()[-k:][::-1]
        
        # Map back to original indices
        top_indices = [filtered_indices[i] for i in top_filtered_indices]
        
        recommendations = []
        for i, idx in enumerate(top_indices):
            assessment = self.assessments[idx]
            recommendations.append({
                'name': assessment['name'],
                'url': assessment['url'],
                'remote_testing': assessment['remote_testing'],
                'adaptive_irt': assessment['adaptive_irt'],
                'duration': assessment['duration'],
                'test_type': assessment['test_type'],
                'description': assessment['description'],
                'score': float(filtered_scores[top_filtered_indices[i]])
            })
        
        return recommendations
    
    def get_test_types(self):
        """Return all available test types"""
        return self.test_types
    
    def get_keywords(self):
        """Return common keywords from assessments"""
        return self.keywords