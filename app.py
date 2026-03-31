import streamlit as st
from groq import Groq

st.set_page_config(page_title="Free DeepSeek Chat", page_icon="🤖")
st.title("DeepSeek-R1 on Groq (Free)")

# Initialize the Groq client using Streamlit Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask DeepSeek anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        # Model ID for DeepSeek-R1 Distill Llama 70B on Groq
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=False # Set to True for real-time typing effect
        )
        
        full_response = response.choices[0].message.content
        st.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})


import streamlit.components.v1 as components

# Define the widget HTML string
widget_code = """
<script src="https://context7.com/widget.js" data-library="/zwelshman/chat_streamlit"></script>
"""

# Embed the widget
# height=0 is often used for invisible or floating widgets, 
# but you can adjust it if the widget needs to render a container.
components.html(widget_code, height=0)

