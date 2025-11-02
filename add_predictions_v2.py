with open('app.py', 'r') as f:
    lines = f.readlines()

# Find "df = load_data()" 
insert_pos = -1
for i, line in enumerate(lines):
    if 'df = load_data()' in line:
        insert_pos = i + 1
        break

if insert_pos == -1:
    print("❌ Could not find 'df = load_data()'")
else:
    prediction_code = '''
# ============= AI PREDICTIONS =============
if isolation_forest is not None and kmeans_model is not None:
    features = ['login_count', 'time_spent', 'quiz_attempts']
    X = df[features]
    
    # Predict anomalies and clusters
    df['anomaly'] = isolation_forest.predict(X)
    df['cluster'] = kmeans_model.predict(X)
    
    # Map clusters to Low/Medium/High based on engagement
    cluster_means = df.groupby('cluster')[features].mean().sum(axis=1)
    cluster_ranking = cluster_means.sort_values().index.tolist()
    cluster_labels = {cluster_ranking[0]: 'Low', cluster_ranking[1]: 'Medium', cluster_ranking[2]: 'High'}
    df['engagement_level'] = df['cluster'].map(cluster_labels)

'''
    lines.insert(insert_pos, prediction_code)
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print(f"✅ AI predictions added at line {insert_pos}!")
