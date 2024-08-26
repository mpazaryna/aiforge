import streamlit as st
from aiforge.lab.unified import UnifiedApis

def main():
    st.title("AI Chat Interface")

    # Sidebar for model selection and API key input
    with st.sidebar:
        provider = st.selectbox(
            "Select AI Provider",
            ["openai", "anthropic", "openrouter"]
        )
        
        api_key = st.text_input("Enter API Key", type="password")
        
        model = st.selectbox(
            "Select Model",
            get_models_for_provider(provider)
        )

    # Main chat interface
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Ask a question"):
        if not api_key:
            st.error("Please enter an API key in the sidebar.")
            return

        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                unified_api = UnifiedApis(
                    provider=provider,
                    api_key=api_key,
                    model=model,
                    stream=True,
                    should_print_init=False
                )
                response = unified_api.chat(prompt, should_print=False)
                message_placeholder.write(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

def get_models_for_provider(provider):
    if provider == "openai":
        return ["gpt-3.5-turbo", "gpt-4"]
    elif provider == "anthropic":
        return ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-2.1"]
    elif provider == "openrouter":
        return ["google/gemini-pro-1.5", "anthropic/claude-3-opus-20240229", "openai/gpt-4-turbo-preview"]
    else:
        return []

if __name__ == "__main__":
    main()