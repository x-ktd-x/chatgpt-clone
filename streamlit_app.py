import openai
import streamlit as st
from google_oauth2_required import google_oauth2_required

# main
@google_oauth2_required
def main():
    with st.sidebar:
        st.title('🤖💬 OpenAI Chatbot')
        # 本番
        if 'OPENAI_API_KEY' in st.secrets:
            st.success('APIキーの取得に成功しました!', icon='✅')
            openai.api_key = st.secrets['OPENAI_API_KEY']
        else:
            st.warning('APIキーの取得に失敗しました', icon='⚠️')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=[{"role": m["role"], "content": m["content"]}
                          for m in st.session_state.messages], stream=True):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# メイン関数の実行
main()