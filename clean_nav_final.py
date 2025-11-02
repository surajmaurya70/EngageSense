import re
with open('app.py', 'r') as f:
    src = f.read()

# Remove top HTML navbar block (the one with Dashboard, Students, Reports, Filters, Export etc)
src = re.sub(r'st\.markdown\(f""".*?""", unsafe_allow_html=True\)', '', src, flags=re.DOTALL)

# Remove Export button everywhere
src = src.replace('st.button("📥 Export")', '')
src = src.replace('st.button("Export")', '')

with open('app.py', 'w') as f:
    f.write(src)
print("✅ Top navbar and Export button removed - only working navigation left!")
