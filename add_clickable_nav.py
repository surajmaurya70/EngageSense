# Read current app.py
with open('app.py', 'r') as f:
    lines = f.readlines()

# Find the HTML navbar and mark for replacement
new_content = []
skip_until = -1

for i, line in enumerate(lines):
    if skip_until > 0 and i < skip_until:
        continue
    
    # Find start of HTML navbar
    if 'st.markdown(f"""' in line and i < 100:
        # Add new button-based navbar
        new_content.append('# Clickable Navigation\n')
        new_content.append('if "current_page" not in st.session_state:\n')
        new_content.append('    st.session_state.current_page = "Dashboard"\n\n')
        new_content.append('col1, col2 = st.columns([3, 2])\n')
        new_content.append('with col1:\n')
        new_content.append('    st.markdown("## 📊 EngageSense | AI-Powered Analytics")\n')
        new_content.append('with col2:\n')
        new_content.append('    c1, c2, c3, c4 = st.columns(4)\n')
        new_content.append('    with c1:\n')
        new_content.append('        if st.button("Dashboard"): st.session_state.current_page = "Dashboard"\n')
        new_content.append('    with c2:\n')
        new_content.append('        if st.button("Students"): st.session_state.current_page = "Students"\n')
        new_content.append('    with c3:\n')
        new_content.append('        if st.button("Reports"): st.session_state.current_page = "Reports"\n')
        new_content.append('    with c4:\n')
        new_content.append('        if st.button("🔔 3"): st.toast("3 new notifications!")\n\n')
        
        # Skip until end of HTML block
        for j in range(i, min(i+50, len(lines))):
            if 'unsafe_allow_html=True)' in lines[j]:
                skip_until = j + 1
                break
    else:
        new_content.append(line)

# Write updated file
with open('app.py', 'w') as f:
    f.writelines(new_content)

print("✅ Updated!")
