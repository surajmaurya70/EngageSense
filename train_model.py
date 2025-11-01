import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

print("📊 Loading data...")
df = pd.read_csv('student_engagement.csv')
print(f"✅ Data loaded: {len(df)} rows")

print("🤖 Training model...")
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(df[['login_count', 'time_spent', 'quiz_attempts']])
print("✅ Model trained successfully!")

print("💾 Saving model...")
joblib.dump(model, 'isolation_forest.pkl')
print("✅ Model saved as isolation_forest.pkl")

print("\n🎉 All done! You can now run: streamlit run app.py")
