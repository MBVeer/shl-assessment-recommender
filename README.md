# SHL Assessment Recommender

An intelligent web application that recommends relevant SHL assessments based on job descriptions. The application uses natural language processing to match job requirements with appropriate assessments from SHL's product catalog.

## Features

- Natural language job description input
- Intelligent assessment matching using TF-IDF and cosine similarity
- Advanced filtering options:
  - Test types
  - Remote testing support
  - Adaptive/IRT support
  - Maximum duration
- Interactive keyword suggestion system
- RESTful API endpoints
- Clean, responsive UI with Tailwind CSS

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/shl-assessment-recommender.git
cd shl-assessment-recommender
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app/app.py
```

5. Access the application at http://localhost:5000

## API Usage

### Get Recommendations

```bash
POST /api/recommend
Content-Type: application/json

{
  "job_description": "Looking for a software developer with Python experience",
  "test_types": ["Technical Knowledge", "Coding"],
  "remote_testing": true,
  "adaptive_irt": true,
  "max_duration": 60
}
```

### Get Test Types

```bash
GET /api/test-types
```

### Get Keywords

```bash
GET /api/keywords
```

## Technologies Used

- Python 3.8+
- Flask
- scikit-learn
- NumPy
- Tailwind CSS
- JavaScript

## Project Structure

```
shl-assessment-recommender/
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── recommendation_engine.py
│   └── templates/
│       └── index.html
├── data/
│   └── assessments.json
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 