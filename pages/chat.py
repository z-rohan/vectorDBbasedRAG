import streamlit as st
from utils import Utillities
from db import DB
from answerMe import Answer


st.set_page_config(page_title="Chat with Document")
st.sidebar.header("Chat with Document")
db_obj = DB()
utils = Utillities()
db = db_obj.get_coll()


print(">>>>>>>>before chat")
if "chat" not in st.session_state:
    print("after chat<<<<<<<<<<")
    st.session_state.chat = Answer().make_model()
    st.session_state.messeges = []
    # model = st.session_state.chat.make_model()

query = st.chat_input("What you want to know from uploaded documwent")
print(query)
if query:
    # st.chat_message('user').markdown(query)
    relavent_docs = db_obj.get_relevant_passage(query)
    prompt = utils.make_prompt(query, relavent_docs)
    st.session_state.messeges.append({'role':'user', 'parts':[query, prompt]})
    response = st.session_state.chat.generate_content(prompt)
    st.session_state.messeges.append({'role':'model', 'parts':[response.text]})
    # st.chat_message('model').markdown(response.text)
    # st.write(st.session_state.messeges)
    for message in st.session_state.messeges:
        with st.chat_message(message.get('role')):
            st.markdown(message.get('parts')[0])

    
