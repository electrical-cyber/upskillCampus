# upskillCampus
# QuizApp

## Overview
**QuizApp** is a modern quiz application built using Python and Tkinter. The app allows users to choose different topics, answer questions, and track their scores. It includes a timer, multiple-choice questions, and provides explanations after each answer.

## Features
- Select from multiple quiz topics using a dropdown menu.
- Multiple-choice questions with shuffled answers.
- Timer for each question, showing time remaining.
- Instant feedback with explanations after each answer.
- Score tracking throughout the quiz.
- Navigation between questions (previous/next).
  File name- quiz_app.py
file structure
QuizApp/
├── quizzes/               # Directory for quiz data in JSON format
├── quiz_app.py            # Main Python application
└── README.md              # Project documentation
json format
[
  {
    "quiz_items": [
      {
        "question": "What is the SI unit of temperature?",
        "answers": ["Kelvin", "Celsius", "Fahrenheit", "Rankine"],
        "correct": 0,
        "source": "Physics Textbook",
        "explanation": "Kelvin is the SI unit of temperature."
      }
    ]
  }
]
Ensure you have the required quiz files in the quizzes/ directory. Each quiz file should follow the format: [topic]_quiz.json.

Run the application:


## Installation
### Prerequisites
- Python 3.x
- Tkinter (comes bundled with Python)
- JSON quiz files (stored in the `quizzes/` directory)



