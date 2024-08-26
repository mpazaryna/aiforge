import streamlit as st
from aiforge.lab.hello_world import greet

def main():
    """
    Main function for the Greeting App.
    
    This Streamlit app demonstrates the usage of the greet function from aiforge.lab.hello_world.
    It allows users to input a name and receive a personalized greeting.
    The app includes a sidebar with a description, API key input, and a footer with a "Made with ❤️" message.
    """
    st.set_page_config(page_title="Greeting App", layout="wide")

    # Sidebar
    st.sidebar.header("About")
    st.sidebar.write("""
    This app demonstrates the `greet` function from the `aiforge.lab.hello_world` module.
    You can enter a name to receive a personalized greeting, or leave it blank for a default greeting.
    
    **Note:** This is a work in progress. 
    
    GitHub: [http://github.com/mpazaryna/aiforge](http://github.com/mpazaryna/aiforge)
    """)

    # OpenAI API Key input
    api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")
    if st.sidebar.button("Save API Key"):
        st.session_state['openai_api_key'] = api_key
        st.sidebar.success("API Key saved!")

    st.title("Greeting App")

    # Input for custom name
    name = st.text_input("Enter a name (optional):", "")

    if st.button("Greet"):
        if name:
            greeting = greet(name)
        else:
            greeting = greet()
        
        st.success(greeting)

    # Display API key status
    if 'openai_api_key' in st.session_state:
        st.sidebar.info("OpenAI API Key is set.")
    else:
        st.sidebar.warning("OpenAI API Key is not set.")

    # Footer
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #0E1117;
            color: #FAFAFA;
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
        </style>
        <div class="footer">Made with ❤️ using Streamlit</div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()