"""
シンプルなチャットアプリを作る
"""
import streamlit as st
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage


def init_page():
    """
    Webページやサイドバーを調整
    """
    #Webページの設定
    st.set_page_config(
        page_title = "My ChatGPT",
        page_icon = "⚽️"
    )
    #ヘッダーの設定
    st.header("My ChatGPT ⚽️")
    st.sidebar.title("Options")


def init_messages():
    """
    履歴を削除
    """
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "message" not in st.session_state:
        st.session_state.messages = [SystemMessage(content="You are a helpful assistant.")]
        st.session_state.costs = []


def select_model():
    """
    モデルの選択
    """
    model = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
    if model == "GPT-3.5":
        model_name = "gpt-3.5-turbo:"
    else:
        model_name = "gpt-4"

    #サイドバーにスライダーを追加
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.1)
    return ChatOpenAI(temperature=temperature, model_name=model_name)


def get_answer(llm, messages):
    with get_openai_callback() as cb:
        answer = llm(messages)
    return answer.content, cb.total_const


def main():
    init_page()

    #llm = select_model()
    #サイドバーにスライダーを追加
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.1)
    llm = ChatOpenAI(temperature=temperature)
    init_messages()

    #ウィジェット
    container = st.container()
    with container:
        #ユーザーが入力できるフォームの作成
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area(label='Message: ', key='input', height=100)
            submit_button = st.form_submit_button(label='Send')
        #何か入力されて Submit ボタンが押されたら実行される
        if submit_button and user_input:
            #ユーザーの入力を監視
            #if user_input := st.chat_input("聞きたいことを入力!"):
            #session_stateはアプリケーションの状態を管理するために使用される
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("ChatGPT is typing ..."):
                response = llm(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))

    #チャット履歴の表示
    messages = st.session_state.get('messages', [])
    for message in messages:
        #チャット履歴表示用のコード
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else: #isinstance(message, SystemMessage):
            st.write(f"System message: {message.content}")

    #料金の計算
    costs = st.session_state.get('costs', [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")

if __name__ == "__main__":
    main()

# #SystemMessageでキャラ設定もできる
# messages = [
#     SystemMessage(content="You ara a helpful assistant."),
#     HumanMessage(content=message)
# ]
