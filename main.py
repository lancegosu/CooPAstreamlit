import streamlit as st
from utils import smart_search, grab_urls, get_citation

st.set_page_config(page_title="CooPA")
st.title("🌱 CooPA")
st.caption("Note: This chatbot does not have memory.")

st.sidebar.write('[My Portfolio](https://lancen.streamlit.app/)')
st.sidebar.caption("Made by [Lance Nguyen](https://www.linkedin.com/in/lancedin/)")

st.sidebar.info(
    """
    Info: CooPA is a chatbot that uses the OpenAI API to deliver contextually informed answers by aggregating relevant content from Google search based on user queries.
    Start by asking anything to the chatbot!
    """
)

with st.sidebar.expander('**My Other Apps**'):
    st.caption('[LLM Optimization with RAG](https://lcrags.streamlit.app/)')
    st.caption('[SpotOn](https://spoton.streamlit.app/)')
    st.caption('[Qdoc](https://qdocst.streamlit.app/)')

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! Ask me anything!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = smart_search(prompt)
    urls = grab_urls(prompt, num_link=3)
    citation = get_citation(urls)
    response_with_citation = f"{response}\n\nSources:\n\n{citation}"
    st.session_state.messages.append({"role": "assistant", "content": response_with_citation})
    st.chat_message("assistant").write(response_with_citation)

if st.button("Refresh Conversation"):
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me anything!"}]
    st.success("Conversation has been refreshed.")
