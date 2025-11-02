import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
import joblib

print("🔄 Loading data...")
df = pd.read_csv('student_engagement.csv')
print(f"✅ Data loaded! Shape: {df.shape}")
print(f"📋 Columns: {list(df.columns)}")

# Select features
features = ['login_count', 'time_spent', 'quiz_attempts']
X = df[features]

print("🎯 Training Isolation Forest...")
clf = IsolationForest(contamination=0.1, random_state=42)
clf.fit(X)
df['anomaly'] = clf.predict(X)

print("🎯 Training K-Means Clustering...")
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X)

print("💾 Saving models...")
joblib.dump(clf, 'isolation_forest.pkl')
joblib.dump(kmeans, 'kmeans_model.pkl')

print("\n📊 SUMMARY:")
# Calculate engagement score if not present
if 'engagement_score' in df.columns:
    avg_eng = df['engagement_score'].mean()
else:
    # Create score from features
    avg_eng = df[features].mean(axis=1).mean()
    
print(f"Avg Engagement: {avg_eng:.2f}")
print(f"\nStudents per cluster:\n{df['cluster'].value_counts().sort_index()}")
print(f"\nAnomaly %: {(df['anomaly'] == -1).mean() * 100:.2f}%")
print("\n✅ Models saved successfully!")
