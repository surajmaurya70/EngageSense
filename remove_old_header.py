with open('app.py', 'r') as f:
    content = f.read()

# Remove old .main-header CSS and HTML
import re

# Remove old header CSS (from .main-header to closing })
content = re.sub(r'\.main-header\s*\{[^}]+\}', '', content)
content = re.sub(r'\.header-content\s*\{[^}]+\}', '', content)
content = re.sub(r'\.logo\s*\{[^}]+\}', '', content)
content = re.sub(r'\.title\s*\{[^}]+\}', '', content)
content = re.sub(r'\.subtitle\s*\{[^}]+\}', '', content)

# Remove old header HTML
content = re.sub(r'<div class="main-header">.*?</div>\s*""", unsafe_allow_html=True\)', '', content, flags=re.DOTALL)

with open('app.py', 'w') as f:
    f.write(content)

print("✅ Old header removed!")
