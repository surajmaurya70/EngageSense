import streamlit.components.v1 as components
import time

def scroll_to_element():
    """Working scroll with unique key each time"""
    timestamp = str(time.time()).replace('.', '')
    components.html(f"""
    <script>
    setTimeout(function() {{
        const h2List = window.parent.document.querySelectorAll('h2');
        for(let h of h2List) {{
            if(h.textContent.includes('Student Data')) {{
                h.scrollIntoView({{behavior:'smooth',block:'start'}});
                break;
            }}
        }}
    }}, 100);
    </script>
    """, height=0, key=f"scroll_{timestamp}")
