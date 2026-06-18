# streamlit run basic_chatbot_frontend.py --server.fileWatcherType none

import streamlit as st
from basic_chatbot_backend import workflow

with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state['message_history'] = []
        st.rerun()


user_role = "user"
assistant_role = "assistant"

st.title("Basic Chatbot")


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
    # box to show message
    with st.chat_message(user_role):
        # put user input in the box
        st.text(user_input)
    initial_state = {'user_query': user_input}
    '''
    # without streaming
    
    response = workflow.invoke(initial_state)
    ai_reply = response['llm_response']
    print('ai_reply', ai_reply)

    st.session_state['message_history'].append({'role': assistant_role, 'content': ai_reply})

    with st.chat_message(assistant_role):
        # put user input in the box
        st.text(ai_reply)
    
    '''

    #  with streaming
    with st.chat_message(assistant_role):
        response_placeholder = st.empty()
        full_response = ""

        for chunk, metadata in workflow.stream(initial_state, stream_mode = "messages"):
            if hasattr(chunk, 'content'):
                full_response+=chunk.content
                # response_placeholder.text(full_response)

    # Store message history in session state
    st.session_state['message_history'].append({'role': user_role, 'content': user_input})
    st.session_state['message_history'].append({'role': assistant_role, 'content': full_response})