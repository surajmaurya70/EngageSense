with open('app.py', 'r') as f:
    content = f.read()

# Find where df is loaded (after @st.cache_data def load_data():)
# Add prediction code after df is created

prediction_code = '''
# ============= AI PREDICTIONS =============
if isolation_forest is not None and kmeans_model is not None:
    features = ['login_count', 'time_spent', 'quiz_attempts']
    X = df[features]
    
    # Predict anomalies and clusters
    df['anomaly'] = isolation_forest.predict(X)
    df['cluster'] = kmeans_model.predict(X)
    
    # Map cluster to labels (based on mean engagement)
    cluster_means = df.groupby('cluster')[features].mean().sum(axis=1)
    cluster_ranking = cluster_means.sort_values().index.tolist()
    cluster_labels = {cluster_ranking[0]: 'Low', cluster_ranking[1]: 'Medium', cluster_ranking[2]: 'High'}
    df['engagement_level'] = df['cluster'].map(cluster_labels)
    
    # Calculate AI metrics
    avg_engagement = df[features].mean(axis=1).mean()
    anomaly_pct = (df['anomaly'] == -1).mean() * 100
    cluster_counts = df['engagement_level'].value_counts()

'''

# Insert after "return df" in load_data function
insert_marker = "return df"
pos = content.find(insert_marker)
if pos != -1:
    # Find the end of return df line
    end_pos = content.find('\n', pos) + 1
    content = content[:end_pos] + prediction_code + content[end_pos:]
    
    with open('app.py', 'w') as f:
        f.write(content)
    print("✅ AI predictions added!")
else:
    print("❌ Could not find 'return df' in load_data function")
