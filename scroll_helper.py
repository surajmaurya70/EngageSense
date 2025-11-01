import streamlit.components.v1 as components

def scroll_to_element():
    """Working scroll without key parameter"""
    components.html("""
    <script>
    setTimeout(function() {
        const h2List = window.parent.document.querySelectorAll('h2');
        for(let h of h2List) {
            if(h.textContent.includes('Student Data')) {
                h.scrollIntoView({behavior:'smooth',block:'start'});
                break;
            }
        }
    }, 200);
    </script>
    """, height=0)
