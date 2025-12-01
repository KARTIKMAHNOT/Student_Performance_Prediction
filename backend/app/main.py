from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
from pydantic import BaseModel
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


try:
    regression_model = joblib.load("ml/regression_model.joblib")
    classification_model = joblib.load("ml/logistic_model.joblib")
    print("✅ Models loaded successfully")
except Exception as e:
    print(f"❌ Error loading models: {e}")


class Features(BaseModel):
    Gender: float
    Study_Hours_per_Week: float
    Attendance_Rate: float
    Past_Exam_Scores: float
    Internet_Access_at_Home: float
    Extracurricular_Activities: float
    Parent_Edu_Bachelors: float
    Parent_Edu_High_School: float
    Parent_Edu_Masters: float
    Parent_Edu_PhD: float


@app.post("/predict-score")
def predict_score(features: Features):
    try:
        data = np.array([[ 
            features.Gender,
            features.Study_Hours_per_Week,
            features.Attendance_Rate,
            features.Past_Exam_Scores,
            features.Internet_Access_at_Home,
            features.Extracurricular_Activities,
            features.Parent_Edu_Bachelors,
            features.Parent_Edu_High_School,
            features.Parent_Edu_Masters,
            features.Parent_Edu_PhD
        ]])

        score = regression_model.predict(data)[0]
        return {"predicted_score": round(float(score), 2)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict-passfail")
def predict_passfail(features: Features):
    try:
        data = np.array([[ 
            features.Gender,
            features.Study_Hours_per_Week,
            features.Attendance_Rate,
            features.Past_Exam_Scores,
            features.Internet_Access_at_Home,
            features.Extracurricular_Activities,
            features.Parent_Edu_Bachelors,
            features.Parent_Edu_High_School,
            features.Parent_Edu_Masters,
            features.Parent_Edu_PhD
        ]])

        pred = classification_model.predict(data)[0]
        prob = classification_model.predict_proba(data)[0][1]

        return {
            "result": "Pass" if pred==1 else "Fail",
            "confidence": f"{prob*100:.2f}%"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class SuggestInput(BaseModel):
    study_hours: float
    attendance: float
    past_score: float
    predicted_score: float

@app.post("/suggestion")
def suggestion(data: SuggestInput):
    try:
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            return {"suggestions": ["Please set HF_TOKEN environment variable"]}

        prompt = f"""
        Student Profile Evaluation:

        • Study Hours/week: {data.study_hours}
        • Attendance: {data.attendance}%
        • Past Score: {data.past_score}
        • Predicted Score: {data.predicted_score}

        Generate 2-3 short, actionable improvement suggestions. Be direct and practical.
        Format each suggestion as a bullet point starting with -.
        """

        api_url = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
        headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 250,
                "temperature": 0.7,
                "do_sample": True,
                "return_full_text": False
            }
        }

        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:

            return get_fallback_suggestions(data)

        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            generated_text = result[0].get('generated_text', '')
        else:
            generated_text = str(result)

        suggestions = parse_suggestions(generated_text)
        
        if not suggestions:
            return get_fallback_suggestions(data)

        return {"suggestions": suggestions[:3]}

    except Exception as e:
        print(f"Error in suggestion endpoint: {e}")
        return get_fallback_suggestions(data)

def parse_suggestions(text: str):
    """Parse the generated text to extract suggestions"""
    suggestions = []
    

    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith(('-', '•', '🔹')) or (line and line[0].isdigit() and '.' in line[:3]):
            clean_line = line.lstrip('-•🔹 ').lstrip('1234567890. ').strip()
            if clean_line and len(clean_line) > 10:  
                suggestions.append(clean_line)
    if not suggestions:
        sentences = text.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 15: 
                suggestions.append(sentence + '.')
    
    return suggestions[:3]  

def get_fallback_suggestions(data: SuggestInput):
    """Provide fallback suggestions when AI fails"""
    suggestions = []
    

    if data.study_hours < 15:
        suggestions.append("Increase study hours to at least 15-20 hours per week for better performance.")
    elif data.study_hours > 30:
        suggestions.append("Consider balancing study time with breaks to avoid burnout.")
    

    if data.attendance < 80:
        suggestions.append("Improve attendance rate to above 80% to benefit from classroom learning.")
    

    if data.predicted_score < data.past_score:
        suggestions.append("Review previous topics where you struggled and focus on understanding core concepts.")
    else:
        suggestions.append("Maintain your current study habits and focus on consistent practice.")
    
    while len(suggestions) < 2:
        suggestions.append("Create a structured study schedule and stick to it consistently.")
    
    return {"suggestions": suggestions[:3]}

@app.get("/")
def home():
    return {"message": "🚀 API Live — Score + Pass/Fail + AI Suggestions Working!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "models_loaded": True}