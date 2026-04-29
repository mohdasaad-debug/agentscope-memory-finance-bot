import streamlit as st
import asyncio

from main import create_agent


st.set_page_config(page_title="Friday Finance Bot")
st.title("💸 Friday - Finance Assistant")

# ------------------------
# init session
# ------------------------
if "agent" not in st.session_state:
    agent, memory, engine = asyncio.run(create_agent("streamlit_user"))

    st.session_state.agent = agent
    st.session_state.memory = memory
    st.session_state.engine = engine
    st.session_state.msg = None
    st.session_state.chat = []


# ------------------------
# chat display
# ------------------------
for role, content in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(content)


# ------------------------
# input
# ------------------------
prompt = st.chat_input("Ask about stocks...")

if prompt:
    st.session_state.chat.append(("user", prompt))

    with st.chat_message("user"):
        st.markdown(prompt)

    async def run():
        msg = st.session_state.msg
        msg = await st.session_state.agent(msg, prompt)
        return msg

    # ⚠️ handle event loop properly
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response_msg = loop.run_until_complete(run())

    st.session_state.msg = response_msg
    reply = response_msg.get_text_content()

    st.session_state.chat.append(("assistant", reply))

    with st.chat_message("assistant"):
        st.markdown(reply)