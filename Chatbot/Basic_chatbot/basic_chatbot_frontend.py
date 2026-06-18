import streamlit as st

with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state['message_history'] = []
        st.rerun()


user_role = "user"
assistant_role = "assistant"

st.title("Basic Chatbot")

# Store message history in session state
# Check if 'message_history' key exists in session state, if not initialize it as an empty list
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
else:
    # loading the conversation history 
    for message in st.session_state['message_history']:
        role = message['role']
        content = message['content']
        # box to show message
        with st.chat_message(role):
            # put user input in the box
            st.text(content)


# input box for user to put query
user_input = st.chat_input('user')
if user_input:
    st.session_state['message_history'].append({'role': user_role, 'content': user_input})
    # box to show message
    with st.chat_message(user_role):
        # put user input in the box
        st.text(user_input)