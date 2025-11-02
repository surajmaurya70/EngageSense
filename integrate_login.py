with open('app.py', 'r') as f:
    lines = f.readlines()

# Find where to insert (after st.set_page_config)
insert_pos = -1
for i, line in enumerate(lines):
    if 'st.set_page_config' in line:
        insert_pos = i + 1
        break

# Login integration code
login_code = '''
# ============= LOGIN SYSTEM =============
from login import show_login_page

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# ============= END LOGIN =============

'''

lines.insert(insert_pos, login_code)

with open('app.py', 'w') as f:
    f.writelines(lines)

print("✅ Login integrated into app.py!")
