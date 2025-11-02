with open('app.py', 'r') as f:
    lines = f.readlines()

# Remove st.set_page_config from wherever it is
filtered = [line for line in lines if 'st.set_page_config' not in line]

# Insert right after imports (line 6: after "from scroll_helper")
insert_pos = 0
for i, line in enumerate(filtered):
    if 'from scroll_helper' in line:
        insert_pos = i + 1
        break

# Insert page config
filtered.insert(insert_pos, '\nst.set_page_config(page_title="EngageSense Analytics", page_icon="📊", layout="wide", initial_sidebar_state="expanded")\n\n')

with open('app.py', 'w') as f:
    f.writelines(filtered)
    
print("✅ st.set_page_config position fixed!")
