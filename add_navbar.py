with open('app.py', 'r') as f:
    lines = f.readlines()

# Find where to add navbar (after login check, before dashboard)
insert_pos = -1
for i, line in enumerate(lines):
    if 'END LOGIN' in line:
        insert_pos = i + 2
        break

if insert_pos == -1:
    print("Error: Could not find insertion point")
else:
    navbar_code = '''
# ============= NAVBAR =============
from navbar import show_navbar
show_navbar()

'''
    lines.insert(insert_pos, navbar_code)
    
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ Navbar integrated!")
