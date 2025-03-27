import streamlit as st

# Simple page config - start with sidebar collapsed
st.set_page_config(
    page_title="Sidebar Test",
    page_icon="🔍",
    initial_sidebar_state="collapsed"
)

# Main content - just the button to show sidebar
st.title("Sidebar Toggle Test")
st.write("This is a minimal test app that shows how to toggle the sidebar.")

# This button shows the sidebar by programmatically clicking the sidebar toggle button
if st.button("☰ SHOW SIDEBAR MENU", use_container_width=True):
    # Use JavaScript to click the sidebar toggle button
    js = """
    <script>
        // Wait for the page to fully load
        setTimeout(function() {
            // Find the sidebar toggle button in the DOM
            const toggleButton = document.querySelector('[data-testid="collapsedControl"]');
            
            // Click it if found
            if (toggleButton) {
                toggleButton.click();
            }
        }, 500);  // Half-second delay to ensure DOM is loaded
    </script>
    """
    st.components.v1.html(js, height=0)
    
# Simple sidebar content
with st.sidebar:
    st.header("Sidebar Menu")
    st.write("This is the sidebar content.")
    st.button("Action Button") 