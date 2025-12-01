import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv("cleaned_regression_dataset.csv")

X = df.drop(columns=["Final_Exam_Score"])
y = df["Final_Exam_Score"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(
    n_estimators=400,
    max_depth=12,
    min_samples_split=5,
    min_samples_leaf=3,
    random_state=42
)
model.fit(X_train, y_train)

pred = model.predict(X_test)

mse = mean_squared_error(y_test, pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, pred)
r2 = r2_score(y_test, pred)

print("\n--- Regression Results ---")
print(f"MSE: {mse:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAE: {mae:.2f}")
print(f"R2 Score: {r2:.4f}")

joblib.dump(model, "regression_model.joblib")
print("📌 Model Saved as regression_model.joblib")

plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
feature_importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=True)
sns.barplot(x=feature_importance.values, y=feature_importance.index, color='skyblue')
plt.title("Feature Importance")
plt.xlabel("Importance Score")

plt.subplot(2, 2, 2)
sns.scatterplot(x=y_test, y=pred, alpha=0.7)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
plt.xlabel("Actual Marks")
plt.ylabel("Predicted Marks")
plt.title("Actual vs Predicted")

plt.subplot(2, 2, 3)
residuals = y_test - pred
sns.histplot(residuals, kde=True, bins=15)
plt.axvline(x=0, color='r', linestyle='--')
plt.xlabel("Residuals")
plt.title("Residual Distribution")

plt.subplot(2, 2, 4)
sns.regplot(x=y_test, y=pred, scatter_kws={'alpha':0.6}, line_kws={'color':'red'})
plt.xlabel("Actual Marks")
plt.ylabel("Predicted Marks")
plt.title("Regression Fit")

plt.tight_layout()
plt.show()

print(f"\n📊 Prediction Stats:")
print(f"Min: {pred.min():.1f}, Max: {pred.max():.1f}")
print(f"Actual Range: {y_test.min():.1f} - {y_test.max():.1f}")

train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
print(f"\n📈 Training Score: {train_score:.4f}")
print(f"📊 Test Score: {test_score:.4f}")
print(f"📉 Overfitting gap: {train_score - test_score:.4f}")
