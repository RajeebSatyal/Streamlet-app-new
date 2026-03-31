import streamlit as st
from prompt_template import Combined_chain
from prompt_template import parallel_chain


st.title('Email Assistant')
email_topic=st.text_input('Email topic')
receipient=st.text_input('Receipient')
name=st.text_input('Name')

def generate_email():
    if not email_topic or not receipient or not name:
        st.error("Please fill in all fields")
        return
    
    email=parallel_chain.invoke({
        "email_topic":email_topic,
        "receipient":receipient,
        "name":name,
        "question":email_topic
    })

    st.write("Subject Line:")
    st.markdown(email['subject_line']['subject_line'])
    st.write("Draft Email:")
    st.markdown(email['combined_chain']['final_email'])


st.button("Generate Email", on_click=generate_email)
