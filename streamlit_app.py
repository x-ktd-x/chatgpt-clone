import openai
import streamlit as st
from google_oauth2_required import google_oauth2_required

# 一応githubのicon消し（そこまでしなくてもいいかも？）
hide_github_icon_style = """
<style>
[data-testid="stToolbarActions"] {
    display: none !important;
}
</style>
"""

# github消しを呼び出す
st.markdown(hide_github_icon_style, unsafe_allow_html=True)

# main
@google_oauth2_required
def main():
    with st.sidebar:
        st.title(':ferry: SS GPT β版')
        # 本番
        if 'OPENAI_API_KEY' in st.secrets:
            st.markdown("""
                    <style>
                        .custom-success {
                        color: #323232;
                        background-color: #E5E5E5;
                        padding: 10px;
                        border-radius: 5px;
                    }
                    </style>
                    <div class="custom-success">
                        ⚓️ API key already provided! ⚓️
                    </div>
                    """, unsafe_allow_html=True)
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
if __name__ == "__main__":
    # Check if the user is authenticated in session state
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    # Apply the CSS again if the user is authenticated (post OAuth)
    if st.session_state['authenticated']:
        st.markdown(hide_github_icon_style, unsafe_allow_html=True)

    main()