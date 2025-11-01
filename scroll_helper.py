import streamlit.components.v1 as components

def scroll_to_element(element_id="data-explorer"):
    """Fast smooth scroll with minimal delay"""
    scroll_js = f"""
    <script>
    (function() {{
        const scrollToTarget = () => {{
            const allH2 = window.parent.document.querySelectorAll('h2');
            for (let h2 of allH2) {{
                if (h2.textContent.includes('Student Data Explorer')) {{
                    h2.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                    return;
                }}
            }}
        }};
        
        if (document.readyState === 'complete') {{
            scrollToTarget();
        }} else {{
            window.addEventListener('load', scrollToTarget);
        }}
    }})();
    </script>
    """
    components.html(scroll_js, height=0)
