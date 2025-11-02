with open('app.py', 'r') as f:
    content = f.read()

# Remove the old HTML navbar completely
import re
content = re.sub(r'st\.markdown\(f""".*?unsafe_allow_html=True\)', '', content, flags=re.DOTALL)

# Remove Export button references
content = content.replace('st.button("📥 Export")', '')
content = content.replace('st.button("Export")', '')

with open('app.py', 'w') as f:
    f.write(content)

print("✅ Cleaned!")
