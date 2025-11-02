with open('app.py', 'r') as f:
    content = f.read()

# Find and fix broken CSS in f-string (double the braces)
import re

# Fix single } in CSS that should be }}
content = re.sub(r'(st\.markdown\(f"""[\s\S]*?<style>[\s\S]*?)(\})([\s\S]*?</style>)', 
                 lambda m: m.group(1) + '}}' + m.group(3), content)

with open('app.py', 'w') as f:
    f.write(content)

print("✅ Syntax fixed!")
