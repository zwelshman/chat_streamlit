import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

st.set_page_config(page_title="Free DeepSeek Chat", page_icon="🤖")

# Inject Context7 widget into parent page by escaping the iframe
components.html(
    """
    <script>
        var script = window.parent.document.createElement('script');
        script.src = 'https://context7.com/widget.js';
        script.setAttribute('data-library', '/zwelshman/chat_streamlit');
        window.parent.document.head.appendChild(script);
    </script>
    """,
    height=0,
)

st.title("DeepSeek-R1 on Groq (Free)")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask DeepSeek anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=False,
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
