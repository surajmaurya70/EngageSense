with open('app.py', 'r') as f:
    content = f.read()

# Find header section (after "## 📊 Dashboard Overview")
logout_code = '''
    # Logout button
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
'''

# Insert before first st.markdown after login check
pos = content.find('st.markdown("## 📊 Dashboard Overview")')
if pos > 0:
    content = content[:pos] + logout_code + '\n    ' + content[pos:]
    with open('app.py', 'w') as f:
        f.write(content)
    print("✅ Logout button added!")
else:
    print("⚠️ Could not find dashboard section")
