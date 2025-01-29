import ollama
import streamlit as st

desired_model = 'deepseek-r1:32b-qwen-distill-q4_K_M'

# session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]


def deepseek_chat(messages: list) -> str:
    try:
        response = ollama.chat(model=desired_model, messages=[

            *messages
        ], stream=False)
        return response["message"]["content"]
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
        return ""


def main():
    st.title('🤖 DeepSeek Chatbot')

    with st.sidebar:
        st.header("📚 User Guide")
        st.markdown("""
        ### How to Use
        1. **Start Chatting**: Type your message in the input box at the bottom of the chat
        2. **Continue Conversation**: The chatbot remembers your conversation, so you can ask follow-up questions
        3. **View History**: Scroll up to see your chat history
        4. **Prompt for Math Problems**: Please reason step by step, and put your final answer within boxed{}.

        ### Tips
        - Be specific with your questions
        - Ask follow-up questions for clarification
        - Use the reset button to start a fresh conversation
        - For math problems, start with the prompt mentioned in **How to Use** Guide.

        ### Need Help?
        If you encounter any issues, try resetting the chat using the button below.
        """)

        if st.button("Reset Chat"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! How can I help you today?"}
            ]
            st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("What's on your mind?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = deepseek_chat(st.session_state.messages)
                if response:
                    st.write(response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
