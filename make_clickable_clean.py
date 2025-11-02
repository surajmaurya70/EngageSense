with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
navbar_found = False

for i, line in enumerate(lines):
    # Find the HTML navbar section
    if 'st.markdown(f"""' in line and not navbar_found and i < 50:
        navbar_found = True
        # Add session state and clickable navigation
        new_lines.append('\n# Session state for navigation\n')
        new_lines.append('if "page" not in st.session_state:\n')
        new_lines.append('    st.session_state.page = "Dashboard"\n\n')
        
        # Keep the HTML navbar but add clickable logic after it
        new_lines.append(line)
        continue
    
    # After the navbar HTML block, add button handlers
    if navbar_found and 'unsafe_allow_html=True)' in line:
        new_lines.append(line)
        new_lines.append('\n# Make tabs clickable\n')
        new_lines.append('col1, col2, col3, col4, col5 = st.columns([2,1,1,1,2])\n')
        new_lines.append('with col2:\n')
        new_lines.append('    if st.button("📊", key="dash_btn", help="Dashboard"):\n')
        new_lines.append('        st.session_state.page = "Dashboard"\n')
        new_lines.append('with col3:\n')
        new_lines.append('    if st.button("👥", key="students_btn", help="Students"):\n')
        new_lines.append('        st.session_state.page = "Students"\n')
        new_lines.append('with col4:\n')
        new_lines.append('    if st.button("📈", key="reports_btn", help="Reports"):\n')
        new_lines.append('        st.session_state.page = "Reports"\n')
        new_lines.append('with col5:\n')
        new_lines.append('    if st.button("🔔 3", key="notif_btn"):\n')
        new_lines.append('        st.toast("3 new notifications!")\n\n')
        navbar_found = False
        continue
    
    new_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Made clickable!")
