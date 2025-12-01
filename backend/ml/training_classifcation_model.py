import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

df = pd.read_csv("cleaned_classification_dataset.csv")

X = df.drop(columns=["Pass_Fail"])
y = df["Pass_Fail"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=300)
model.fit(X_train, y_train)

pred = model.predict(X_test)

print(f"\nAccuracy: {accuracy_score(y_test, pred)*100:.2f}%")
print("\nClassification Report:\n", classification_report(y_test, pred))

joblib.dump(model, "logistic_model.joblib")
print("\n📌 Logistic Model Saved as logistic_model.joblib")

cm = confusion_matrix(y_test, pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Greens")
plt.title("Confusion Matrix - Logistic Regression")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()
