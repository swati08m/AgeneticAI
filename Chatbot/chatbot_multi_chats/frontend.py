import streamlit as st
import uuid
from backend import workflow
def create_unique_uuid():
    return str(uuid.uuid4())

# STEP 1: CREATE SESSION VARIABLES (ONLY FIRST TIME)
# chats = {chat_id_1 : [messages], chat_id_2 : [messages]}
if 'chats' not in st.session_state:
    # create first chat automatically
    first_chat_id = create_unique_uuid() # first chat id
    st.session_state.chats = {first_chat_id:[]}
    # Track which chat is currently selected
    st.session_state.current_chat = first_chat_id

# STEP 2: SIDEBAR
with st.sidebar:
    st.title('Chats')
    # ---------------- # Create New Chat # ------------------------
    if st.button('New Chat'):
        # Generate unique chat id
        new_chat_id = create_unique_uuid()
        # Create empty conversation
        st.session_state.chats[new_chat_id]=[]
        # Switch to newly created chat
        st.session_state.current_chat = new_chat_id
        st.rerun()
    st.divider() # create divider line


    # ---------------------------- # Show all chats in sidebar # ---------------------------
    for chatid in st.session_state.chats.keys():
        if st.button(chatid):
            # Switch to selected chat
            st.session_state.current_chat = chatid
            st.rerun()
    st.divider()  # create divider line

    # ----------------------------  # Clear Currenr chat # ---------------------------
    if st.button('Clear Chat'):
        current_chat = st.session_state.current_chat
        st.session_state.chats[current_chat] = []
        st.rerun()

# STEP 3: MAIN PAGE TITLE
st.title('ChatBot')

# STEP 4: LOAD CURRENT CHAT id
current_chat = st.session_state.current_chat

# STEP 5: DISPLAY OLD CHAT HISTORY
for msg_dict in st.session_state.chats[current_chat]:
    role = msg_dict['role']
    content = msg_dict['content']
    with st.chat_message(role):
        st.text(content)

# LangGraph Thread ID # # Each chat gets separate memory # Similar to ChatGPT conversation
Config = {'configurable':{'thread_id':current_chat}}

# STEP 6: USER INPUT
user_input = st.chat_input('ask anything')
if user_input:
    # Show user message immediately
    with st.chat_message('user'):
        st.text(user_input)

    # Save user message
    msg_dict = {'role':'user', 'content':user_input}
    st.session_state.chats[current_chat].append(msg_dict)

    initial_state={'user_query':user_input}
    with st.chat_message('assistant'):
        # response = workflow.invoke(initial_state)
        # ai_reply = response['llm_response']
        # st.text(ai_reply)
        response_placeholder = st.empty()
        ai_reply = ""
        for chunk, metadata in workflow.stream(initial_state, stream_mode="messages"):
            if hasattr(chunk, 'content'):
                ai_reply+=chunk.content
                response_placeholder.text(ai_reply)
        # Save llm reply
        msg_dict = {'role': 'assistant', 'content': ai_reply}
        st.session_state.chats[current_chat].append(msg_dict)

    print("st.session_state.chats", st.session_state.chats)












