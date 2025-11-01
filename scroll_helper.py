import streamlit.components.v1 as components
import random

def scroll_to_element():
    """Scroll with unique random ID each time"""
    random_id = random.randint(100000, 999999)
    components.html(f"""
    <div id="scroll-trigger-{random_id}"></div>
    <script>
    setTimeout(function() {{
        const h2List = window.parent.document.querySelectorAll('h2');
        for(let h of h2List) {{
            if(h.textContent.includes('Student Data')) {{
                h.scrollIntoView({{behavior:'smooth',block:'start'}});
                break;
            }}
        }}
    }}, 200);
    </script>
    """, height=0)
