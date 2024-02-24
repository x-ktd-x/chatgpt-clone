import openai
import streamlit as st

# GitHubアイコンを隠す
hide_github_icon_style = """
<style>
[data-testid="stToolbarActions"] {
    display: none !important;
}
</style>
"""

# GitHubアイコンを隠すスタイルを適用
st.markdown(hide_github_icon_style, unsafe_allow_html=True)

# main関数
def main():
    with st.sidebar:
        st.title(':ferry: SS GPT β版')
        # APIキーの確認
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

    # メッセージの初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # メッセージの表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # チャット入力
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# メイン関数の実行
if __name__ == "__main__":
    main()