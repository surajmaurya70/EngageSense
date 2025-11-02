# Read existing app.py
with open('app.py', 'r') as f:
    content = f.read()

# Find where navbar is called
navbar_index = content.find('show_navbar()')

# Insert after navbar, before main content
insertion_point = content.find("if 'theme' not in st.session_state:")

new_navigation = '''
# Initialize page state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'

'''

# Insert navigation state
content = content[:insertion_point] + new_navigation + content[insertion_point:]

# Save
with open('app.py', 'w') as f:
    f.write(content)

print("✅ Updated app.py with page state!")
