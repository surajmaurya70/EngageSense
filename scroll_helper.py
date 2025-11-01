import streamlit.components.v1 as components

def scroll_to_element(element_id="data-explorer", delay=300):
    """
    Smooth scroll to any element on the page
    Args:
        element_id: ID of element to scroll to
        delay: Delay in milliseconds before scrolling
    """
    scroll_js = f"""
    <script>
    setTimeout(function() {{
        const targetElement = window.parent.document.getElementById('{element_id}');
        if (targetElement) {{
            targetElement.scrollIntoView({{ 
                behavior: 'smooth', 
                block: 'start',
                inline: 'nearest'
            }});
        }} else {{
            // Fallback: scroll to element by text content
            const allElements = window.parent.document.querySelectorAll('h2');
            allElements.forEach(function(el) {{
                if (el.textContent.includes('Student Data Explorer')) {{
                    el.scrollIntoView({{ 
                        behavior: 'smooth', 
                        block: 'start' 
                    }});
                }}
            }});
        }}
    }}, {delay});
    </script>
    """
    components.html(scroll_js, height=0)

def scroll_to_bottom(delay=200):
    """Scroll to bottom of page"""
    scroll_js = f"""
    <script>
    setTimeout(function() {{
        window.parent.scrollTo({{
            top: window.parent.document.body.scrollHeight,
            behavior: 'smooth'
        }});
    }}, {delay});
    </script>
    """
    components.html(scroll_js, height=0)

def scroll_to_top(delay=200):
    """Scroll to top of page"""
    scroll_js = f"""
    <script>
    setTimeout(function() {{
        window.parent.scrollTo({{
            top: 0,
            behavior: 'smooth'
        }});
    }}, {delay});
    </script>
    """
    components.html(scroll_js, height=0)
