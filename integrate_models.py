with open('app.py', 'r') as f:
    lines = f.readlines()

# Remove duplicate st.set_page_config (line 9)
fixed_lines = []
seen_page_config = False
for line in lines:
    if 'st.set_page_config' in line:
        if not seen_page_config:
            # Keep only first occurrence with expanded sidebar
            fixed_lines.append('st.set_page_config(page_title="EngageSense Analytics", page_icon="📊", layout="wide", initial_sidebar_state="expanded")\n')
            seen_page_config = True
    else:
        fixed_lines.append(line)

# Find position after imports (after line 6: from scroll_helper import...)
insert_pos = 0
for i, line in enumerate(fixed_lines):
    if 'from scroll_helper' in line:
        insert_pos = i + 1
        break

# Model loading code
model_code = '''
# ============= AI MODEL LOADING =============
@st.cache_resource(show_spinner=False)
def load_ai_models():
    """Load trained ML models for anomaly detection and clustering"""
    try:
        isolation_forest = joblib.load('isolation_forest.pkl')
        kmeans_model = joblib.load('kmeans_model.pkl')
        return isolation_forest, kmeans_model
    except FileNotFoundError:
        return None, None

isolation_forest, kmeans_model = load_ai_models()

'''

# Insert model loading after imports
fixed_lines.insert(insert_pos, model_code)

# Write back
with open('app.py', 'w') as f:
    f.writelines(fixed_lines)

print("✅ Step 1: Model loading added!")
print("✅ Step 2: Duplicate set_page_config fixed!")
