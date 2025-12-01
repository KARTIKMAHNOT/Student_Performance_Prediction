import pandas as pd
import numpy as np

np.random.seed(42)

def generate_high_variance_students(n=2000):
    ids=[f"S{str(i).zfill(4)}" for i in range(1,n+1)]
    gender=np.random.choice(["Male","Female"],n,p=[0.48,0.52])

    segments=np.random.choice([0,1,2,3,4],n,p=[0.07,0.18,0.45,0.20,0.10])

    study=[]
    attend=[]
    past=[]
    for s in segments:
        if s==0:
            study.append(np.random.normal(6,5))
            attend.append(np.random.normal(60,10))
            past.append(np.random.normal(50,8))
        elif s==1:
            study.append(np.random.normal(14,6))
            attend.append(np.random.normal(72,8))
            past.append(np.random.normal(62,6))
        elif s==2:
            study.append(np.random.normal(22,7))
            attend.append(np.random.normal(82,7))
            past.append(np.random.normal(72,6))
        elif s==3:
            study.append(np.random.normal(30,6))
            attend.append(np.random.normal(90,4))
            past.append(np.random.normal(85,4))
        else:
            study.append(np.random.normal(34,5))
            attend.append(np.random.normal(96,3))
            past.append(np.random.normal(92,3))

    study=np.clip(study,1,45)
    attend=np.clip(attend,40,100)
    past=np.clip(past,35,100)

    edu_levels=["High School","Bachelors","Masters","PhD"]
    parental=[]
    for s in segments:
        if s==0: p=[0.45,0.35,0.15,0.05]
        elif s==1: p=[0.35,0.40,0.20,0.05]
        elif s==2: p=[0.25,0.40,0.25,0.10]
        elif s==3: p=[0.15,0.35,0.35,0.15]
        else: p=[0.08,0.25,0.40,0.27]
        parental.append(np.random.choice(edu_levels,p=p))

    internet=np.where(np.random.rand(n)<0.85,"Yes","No")
    extra=np.where(np.random.rand(n)<0.55,"Yes","No")

    edu_bonus=np.array([10 if e=="PhD" else 7 if e=="Masters" else 4 if e=="Bachelors" else 0 for e in parental])
    internet_bonus=np.where(internet=="Yes",4,-3)

    final_score=(0.30*np.array(past)+0.29*np.array(attend)+0.40*np.array(study)+1.3*edu_bonus+1.2*internet_bonus+np.random.normal(0,3,n))

    
    final_score=np.clip(final_score,20,100).round(1)
    pass_fail=np.where(final_score>=50,"Pass","Fail")

    df=pd.DataFrame({
        "Student_ID":ids,"Gender":gender,"Study_Hours_per_Week":study,
        "Attendance_Rate":attend,"Past_Exam_Scores":past,"Parental_Education_Level":parental,
        "Internet_Access_at_Home":internet,"Extracurricular_Activities":extra,
        "Final_Exam_Score":final_score,"Pass_Fail":pass_fail})
    return df

df=generate_high_variance_students(2000)
df.to_csv("high_variance_student_dataset.csv",index=False)
df.head()
