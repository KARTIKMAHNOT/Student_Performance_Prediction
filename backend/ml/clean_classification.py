import pandas as pd

df = pd.read_csv("high_variance_student_dataset.csv")

print("\n===== CLASSIFICATION CLEANING STARTED =====")
df = df.drop(columns=["Student_ID", "Final_Exam_Score"], errors="ignore")
df = pd.get_dummies(df, columns=['Parental_Education_Level'], prefix='Parent_Edu')

df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})
df['Internet_Access_at_Home'] = df['Internet_Access_at_Home'].map({'Yes': 1, 'No': 0})
df['Extracurricular_Activities'] = df['Extracurricular_Activities'].map({'Yes': 1, 'No': 0})

df['Pass_Fail'] = df['Pass_Fail'].map({'Pass': 1, 'Fail': 0})   # Correct version

df = df.drop_duplicates()
print("dataset shape:",{df.shape})
df.to_csv("cleaned_classification_dataset.csv", index=False)
print("🚀 Dataset saved!")
