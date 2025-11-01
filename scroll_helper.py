import streamlit.components.v1 as components
import random

def scroll_to_element():
    """Ultra fast scroll - 50ms delay only"""
    random_id = random.randint(100000, 999999)
    components.html(f"""
    <div id="s{random_id}"></div>
    <script>
    setTimeout(()=>{{
        window.parent.document.querySelectorAll('h2').forEach(h=>{{
            if(h.textContent.includes('Student Data')){{
                h.scrollIntoView({{behavior:'smooth',block:'start'}});
            }}
        }});
    }},50);
    </script>
    """, height=0)
