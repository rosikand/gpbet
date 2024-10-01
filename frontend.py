import streamlit as st
from backend import BackendInterface



st.title("GPbeT")
st.text("Chatbot for sports and sports betting analytics with natural language processing. Supports NHL and NBA currently. Must enter only one player name at a time.")
st.text("Note: if you want to ask a query about a new player instead of a follow-up question, please refresh the page.")
st.text("Example 1: 'Will Seth Jones get more than 25.25 minutes on ice in his next game?'")
st.text("Example 2: 'Will Kevin Durant get a combined total of 35 points + rebounds + assists in his next game?'")



if 'backend_int' not in st.session_state:
    st.session_state.backend_int = BackendInterface()


if 'messages' not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Enter your prompt containing a valid current player name or a follow up question from a previous response..."):
    # user 
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # response 
    with st.spinner("Answering question..."):
        if len(st.session_state.messages) <= 1:
            response = st.session_state.backend_int.get_result_single(prompt)
        else:
            response = st.session_state.backend_int.get_followup_response(prompt)

        st.session_state.messages.append({"role": "AI", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)
