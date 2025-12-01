import pandas as pd

df = pd.read_csv("high_variance_student_dataset.csv")

print("\n===== REGRESSION CLEANING STARTED =====")
df = df.drop(columns=["Student_ID", "Pass_Fail"], errors="ignore")
df = pd.get_dummies(df, columns=['Parental_Education_Level'], prefix='Parent_Edu')
df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})
df['Internet_Access_at_Home'] = df['Internet_Access_at_Home'].map({'Yes': 1, 'No': 0})
df['Extracurricular_Activities'] = df['Extracurricular_Activities'].map({'Yes': 1, 'No': 0})
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
df = df.drop_duplicates()

print(f"📊 Final dataset shape: {df.shape}")
df.to_csv("cleaned_regression_dataset.csv", index=False)
print("🚀 Dataset saved!")