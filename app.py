import os
import streamlit as st
from dotenv import load_dotenv

# ---- 環境変数読み込み（Lesson準拠）----
load_dotenv()  # .env の OPENAI_API_KEY を読み込む

# ---- LangChain（Lesson8 準拠の最小構成）----
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

# ====== 画面 ======
st.set_page_config(page_title="Streamlit LLM App", page_icon="💬")
st.title("💬 LLMアプリ（課題）")
st.write("テキストを入力し、専門家の役割を選んで回答を生成します。")

role = st.radio(
    "専門家を選択：",
    ["キャリアコーチ", "栄養士"],
    horizontal=True,
)

user_text = st.text_area("質問・相談内容", height=140, placeholder="例）転職で悩んでいます。")

# ====== 役割ごとのシステムメッセージ（条件：選択値で切替） ======
SYSTEM_MESSAGES = {
    "キャリアコーチ": "あなたは経験豊富なキャリアコーチです。事実に基づき、実行可能な次の一歩を具体的に提示してください。箇条書きを交え、過度に断定せず丁寧に助言してください。",
    "栄養士": "あなたは管理栄養士です。栄養学の基本原則に基づき、健康的で現実的な提案を行います。注意点・代替案も簡潔に示してください。医療行為の助言は避けます。",
}

# ====== LLMへの問い合わせを行う関数（条件：関数化） ======
def ask_llm(text: str, role_name: str) -> str:
    system_msg = SYSTEM_MESSAGES.get(role_name, "")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_msg),
            ("user", "{question}"),
        ]
    )
    # モデルは自由選択可（課題条件）。推奨：gpt-4o-mini / 代替：gpt-3.5-turbo
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"question": text})

# ====== 実行 ======
if st.button("回答を生成"):
    if not user_text.strip():
        st.warning("テキストを入力してください。")
    else:
        with st.spinner("LLMに問い合わせ中..."):
            try:
                answer = ask_llm(user_text, role)
                st.success("回答")
                st.write(answer)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

# 使い方の明示（条件：概要/操作説明）
with st.expander("このアプリについて / 使い方"):
    st.markdown(
        """
- 入力欄に質問・相談内容を記入  
- 「専門家」を選び **回答を生成** をクリック  
- 役割に応じてシステムメッセージを切り替え、LangChain経由でOpenAIに問い合わせます  
- APIキーは `.env` から読み込みます（GitHubには含めません）
        """
    )
