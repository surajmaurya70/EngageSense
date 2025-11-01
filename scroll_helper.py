import streamlit.components.v1 as components

def scroll_to_element():
    """Ultra-fast instant scroll"""
    components.html("""
    <script>
    window.parent.document.querySelectorAll('h2').forEach(h => {
        if(h.textContent.includes('Student Data')) {
            h.scrollIntoView({behavior:'instant',block:'start'});
        }
    });
    </script>
    """, height=0)
