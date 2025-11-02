# Restore and clean integration
with open('app.py', 'r') as f:
    lines = f.readlines()

# 1. Add login after st.set_page_config
for i, line in enumerate(lines):
    if 'st.set_page_config' in line:
        login_code = '''
from login import show_login_page

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_login_page()
    st.stop()

from navbar import show_navbar
show_navbar()

'''
        lines.insert(i + 1, login_code)
        break

# 2. Add AI model loading after imports
for i, line in enumerate(lines):
    if 'from scroll_helper' in line:
        model_code = '''
@st.cache_resource(show_spinner=False)
def load_ai_models():
    try:
        isolation_forest = joblib.load('isolation_forest.pkl')
        kmeans_model = joblib.load('kmeans_model.pkl')
        return isolation_forest, kmeans_model
    except FileNotFoundError:
        return None, None

isolation_forest, kmeans_model = load_ai_models()

'''
        lines.insert(i + 1, model_code)
        break

# 3. Add predictions after df = load_data()
for i, line in enumerate(lines):
    if 'df = load_data()' in line:
        pred_code = '''
if isolation_forest is not None and kmeans_model is not None:
    features = ['login_count', 'time_spent', 'quiz_attempts']
    X = df[features]
    df['anomaly'] = isolation_forest.predict(X)
    df['cluster'] = kmeans_model.predict(X)
    cluster_means = df.groupby('cluster')[features].mean().sum(axis=1)
    cluster_ranking = cluster_means.sort_values().index.tolist()
    cluster_labels = {cluster_ranking[0]: 'Low', cluster_ranking[1]: 'Medium', cluster_ranking[2]: 'High'}
    df['engagement_level'] = df['cluster'].map(cluster_labels)

'''
        lines.insert(i + 1, pred_code)
        break

with open('app.py', 'w') as f:
    f.writelines(lines)

print("✅ Clean integration complete!")
